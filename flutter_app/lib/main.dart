import 'dart:async';
import 'package:flutter/material.dart';
import 'services/dengue_api.dart';
import 'services/notification_service.dart';
import 'services/weather_service.dart';
import 'package:geolocator/geolocator.dart';

// 🗺️ Map
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NotificationService.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Dengue Shield",
      theme: ThemeData(
        primarySwatch: Colors.teal,
        scaffoldBackgroundColor: const Color(0xFFF4F6FA),
      ),
      home: const DengueRiskPage(),
    );
  }
}

class DengueRiskPage extends StatefulWidget {
  const DengueRiskPage({super.key});

  @override
  State<DengueRiskPage> createState() => _DengueRiskPageState();
}

class _DengueRiskPageState extends State<DengueRiskPage> {
  String riskText = "No prediction yet";
  Color riskColor = Colors.grey;
  IconData riskIcon = Icons.help_outline;

  double lowProb = 0.0;
  double mediumProb = 0.0;
  double highProb = 0.0;

  String confidenceText = "—";
  Color confidenceColor = Colors.grey;

  List<String> explanations = [];

  String alertMessage = "";
  bool showAlert = false;

  bool isLoading = false;
  String? errorMessage;

  LatLng? currentLocation;
  bool locationLoading = true;

  Timer? autoCheckTimer;

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();

    autoCheckTimer = Timer.periodic(
      const Duration(hours: 1),
      (timer) => _predictRisk(),
    );
  }

  @override
  void dispose() {
    autoCheckTimer?.cancel();
    super.dispose();
  }

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
      appBar: AppBar(
        title: const Text("Dengue Risk Prediction"),
        centerTitle: true,
      ),
      body: Column(
        children: [
          /// 🗺️ MAP
          Expanded(
            flex: 2,
            child: FlutterMap(
              options: MapOptions(
                initialCenter: mapLocation,
                initialZoom: 12,
              ),
              children: [
                TileLayer(
                  urlTemplate:
                      "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                  userAgentPackageName: 'lk.ac.student.dengue_risk_app',
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

          /// 📊 UI
          Expanded(
            flex: 3,
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Card(
                    elevation: 6,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16)),
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        children: [
                          Icon(riskIcon, size: 60, color: riskColor),
                          const SizedBox(height: 10),

                          Text(
                            riskText,
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 22,
                              fontWeight: FontWeight.bold,
                              color: riskColor,
                            ),
                          ),

                          const SizedBox(height: 10),

                          const Text(
                            "AI-Based Dengue Risk Assessment",
                            style: TextStyle(fontWeight: FontWeight.w600),
                          ),

                          const SizedBox(height: 10),

                          Text(
                            "Prediction Confidence: $confidenceText",
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: confidenceColor,
                            ),
                          ),

                          const SizedBox(height: 20),

                          _probBar("Low Risk", lowProb, Colors.green),
                          _probBar("Medium Risk", mediumProb, Colors.orange),
                          _probBar("High Risk", highProb, Colors.red),

                          /// 🧠 Explainable AI (UNCHANGED)
                          if (explanations.isNotEmpty) ...[
                            const SizedBox(height: 20),
                            const Divider(),
                            const Text(
                              "Why this risk?",
                              style: TextStyle(
                                  fontWeight: FontWeight.bold, fontSize: 16),
                            ),
                            const SizedBox(height: 10),

                            ...explanations.map((e) => ListTile(
                                  leading: const Icon(Icons.info,
                                      color: Colors.blue),
                                  title: Text(e),
                                )),
                          ]
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 20),

                  if (errorMessage != null)
                    Text(errorMessage!,
                        style: const TextStyle(color: Colors.red)),

                  if (isLoading) const CircularProgressIndicator(),

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

  Widget _probBar(String label, double value, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text("$label: ${(value * 100).toStringAsFixed(1)}%"),
        LinearProgressIndicator(
          value: value.clamp(0.0, 1.0),
          minHeight: 10,
          backgroundColor: Colors.grey.shade300,
          valueColor: AlwaysStoppedAnimation(color),
        ),
        const SizedBox(height: 10),
      ],
    );
  }

  /// 🔮 REAL WEATHER + WEEKLY AGGREGATION (FIXED)
  Future<void> _predictRisk() async {
    if (currentLocation == null) return;

    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final weather = await WeatherService.getWeeklyWeather(
        mapLocation.latitude,
        mapLocation.longitude,
      );

      final payload = {
        ..._basePayload(),
        ...weather, // ✅ real weather merged here
      };

      final result = await ApiService.predictRisk(payload);

      setState(() {
        lowProb = result["low_risk_prob"];
        mediumProb = result["medium_risk_prob"];
        highProb = result["high_risk_prob"];

        alertMessage = result["alert_message"];
        showAlert = result["alert"];

        _calculateConfidence();
        _setRiskUI(result["risk_level"]);
      });

      if (showAlert) {
        _showAlertDialog();
        await NotificationService.showNotification(
          "Dengue Risk Alert 🚨",
          alertMessage,
        );
      }
    } catch (e) {
      setState(() {
        errorMessage = "Failed to fetch weather or server error";
      });
    } finally {
      setState(() => isLoading = false);
    }
  }

  void _showAlertDialog() {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text("Dengue Alert"),
        content: Text(alertMessage),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("OK"),
          )
        ],
      ),
    );
  }

  void _calculateConfidence() {
    double maxProb =
        [lowProb, mediumProb, highProb].reduce((a, b) => a > b ? a : b);

    if (maxProb >= 0.75) {
      confidenceText = "High Confidence";
      confidenceColor = Colors.green;
    } else if (maxProb >= 0.5) {
      confidenceText = "Medium Confidence";
      confidenceColor = Colors.orange;
    } else {
      confidenceText = "Low Confidence";
      confidenceColor = Colors.red;
    }
  }

  /// 🧠 Explainable AI (UNCHANGED)
  void _setRiskUI(int risk) {
    if (risk == 0) {
      riskText = "LOW RISK\n🟢 Safe conditions";
      riskColor = Colors.green;
      riskIcon = Icons.check_circle;

      explanations = [
        "Dengue cases in your area are currently low",
        "Rainfall is not enough for mosquito breeding",
        "No outbreak signals detected",
        "Weather conditions are unfavorable for spread",
      ];
    } else if (risk == 1) {
      riskText = "MEDIUM RISK\n🟡 Be cautious";
      riskColor = Colors.orange;
      riskIcon = Icons.warning_amber;

      explanations = [
        "Dengue cases are slightly increasing nearby",
        "Recent rainfall may support mosquito breeding",
        "Temperature supports mosquito activity",
        "Remove stagnant water around your home",
      ];
    } else {
      riskText = "HIGH RISK\n🔴 Take precautions";
      riskColor = Colors.red;
      riskIcon = Icons.error;

      explanations = [
        "High dengue cases reported in your area",
        "Heavy rainfall has created breeding sites",
        "Weather strongly supports transmission",
        "Use mosquito repellent and seek medical advice if needed",
      ];
    }
  }

  Map<String, dynamic> _basePayload() => {
        "Latitude": mapLocation.latitude,
        "Longitude": mapLocation.longitude,

        // keep lag features
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

  Future<void> _getCurrentLocation() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      setState(() {
        locationLoading = false;
        errorMessage = "Location services are disabled.";
      });
      return;
    }

    permission = await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.denied) {
      setState(() {
        locationLoading = false;
        errorMessage = "Location permission denied.";
      });
      return;
    }

    if (permission == LocationPermission.deniedForever) {
      setState(() {
        locationLoading = false;
        errorMessage = "Location permanently denied.";
      });
      return;
    }

    final pos = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high);

    setState(() {
      currentLocation = LatLng(pos.latitude, pos.longitude);
      locationLoading = false;
    });
  }
}