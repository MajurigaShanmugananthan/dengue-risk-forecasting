import 'package:flutter/material.dart';
import 'services/dengue_api.dart';
import 'package:geolocator/geolocator.dart';

// 🗺️ Map packages
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: TestPage(),
    );
  }
}

class TestPage extends StatefulWidget {
  const TestPage({super.key});

  @override
  State<TestPage> createState() => _TestPageState();
}

class _TestPageState extends State<TestPage> {
  // 🔮 Risk UI
  String riskText = "No prediction yet";
  Color riskColor = Colors.grey;
  IconData riskIcon = Icons.help_outline;

  bool isLoading = false;
  String? errorMessage;

  // 📍 GPS state
  LatLng? currentLocation;
  bool locationLoading = true;

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
  }

  // 📍 Fallback = Colombo
  LatLng get mapLocation =>
      currentLocation ?? const LatLng(6.9271, 79.8612);

  @override
  Widget build(BuildContext context) {
    if (locationLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      backgroundColor: const Color(0xFFF4F6FA),
      appBar: AppBar(
        title: const Text("Dengue Risk Prediction"),
        centerTitle: true,
      ),
      body: Column(
        children: [
          // 🗺️ MAP
          Expanded(
            flex: 2,
            child: FlutterMap(
              options: MapOptions(
                initialCenter: mapLocation,
                initialZoom: 12,
              ),
              children: [
                TileLayer(
                  // ✅ FIXED TILE SERVER (NO subdomains)
                  urlTemplate:
                      "https://tile.openstreetmap.org/{z}/{x}/{y}.png",

                  // ✅ REQUIRED by OSM
                  userAgentPackageName:
                      'lk.ac.student.dengue_risk_app',

                  // ✅ Prevent request flooding
                  maxZoom: 18,
                ),
                MarkerLayer(
                  markers: [
                    Marker(
                      point: mapLocation,
                      width: 40,
                      height: 40,
                      child: Icon(
                        riskIcon,
                        color: riskColor,
                        size: 40,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // 📊 UI
          Expanded(
            flex: 3,
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Card(
                    elevation: 6,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        children: [
                          Icon(riskIcon, size: 60, color: riskColor),
                          const SizedBox(height: 15),
                          Text(
                            riskText,
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: riskColor,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  if (isLoading) const CircularProgressIndicator(),

                  if (errorMessage != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 10),
                      child: Text(
                        errorMessage!,
                        style: const TextStyle(color: Colors.red),
                      ),
                    ),

                  const SizedBox(height: 20),

                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.analytics),
                      label: const Text("Predict Dengue Risk"),
                      onPressed: isLoading ? null : _predictRisk,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // 📍 GPS
  Future<void> _getCurrentLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      setState(() {
        errorMessage = "📍 Location services are disabled";
        locationLoading = false;
      });
      return;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.denied ||
        permission == LocationPermission.deniedForever) {
      setState(() {
        errorMessage = "📍 Location permission denied";
        locationLoading = false;
      });
      return;
    }

    final position = await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );

    print("GPS => ${position.latitude}, ${position.longitude}");

    setState(() {
      currentLocation = LatLng(position.latitude, position.longitude);
      locationLoading = false;
    });
  }

  // 🔮 API call
  Future<void> _predictRisk() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final payload = {
        "tavg": 28.4,
        "tmin": 24.1,
        "tmax": 31.2,
        "prcp": 12.5,
        "wspd": 2.1,
        "Latitude": mapLocation.latitude,
        "Longitude": mapLocation.longitude,
        "Dengue_Cases_lag_1": 5,
        "prcp_lag_1": 12.3,
        "tavg_lag_1": 28.1,
        "Dengue_Cases_lag_2": 4,
        "prcp_lag_2": 8.1,
        "tavg_lag_2": 27.9,
        "Dengue_Cases_lag_3": 6,
        "prcp_lag_3": 15.6,
        "tavg_lag_3": 28.6,
        "Dengue_Cases_lag_4": 3,
        "prcp_lag_4": 9.4,
        "tavg_lag_4": 27.5
      };

      final result = await ApiService.predictRisk(payload);
      final int risk = result["risk_level"];

      setState(() {
        if (risk == 0) {
          riskText = "LOW RISK\n🟢 Safe conditions";
          riskColor = Colors.green;
          riskIcon = Icons.check_circle;
        } else if (risk == 1) {
          riskText = "MEDIUM RISK\n🟡 Be cautious";
          riskColor = Colors.orange;
          riskIcon = Icons.warning_amber;
        } else {
          riskText = "HIGH RISK\n🔴 Take precautions";
          riskColor = Colors.red;
          riskIcon = Icons.error;
        }
      });
    } catch (e) {
      setState(() {
        errorMessage = "⚠️ Unable to connect to prediction server";
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }
}
