import 'dart:convert';
import 'package:http/http.dart' as http;

class ClimateService {
  static Future<Map<String, dynamic>> getClimate(
      double lat, double lon) async {
    final url =
        "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon"
        "&current_weather=true"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        "&timezone=auto";

    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);

      final daily = data["daily"];

      double tmax = daily["temperature_2m_max"][0];
      double tmin = daily["temperature_2m_min"][0];
      double prcp = daily["precipitation_sum"][0];
      double wspd = daily["windspeed_10m_max"][0];

      double tavg = (tmax + tmin) / 2;

      return {
        "tavg": tavg,
        "tmin": tmin,
        "tmax": tmax,
        "prcp": prcp,
        "wspd": wspd,
      };
    } else {
      throw Exception("Failed to load climate data");
    }
  }
}