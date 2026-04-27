import 'dart:convert';
import 'package:http/http.dart' as http;

class WeatherService {
  static Future<Map<String, dynamic>> getWeeklyWeather(
      double lat, double lon) async {

    final url =
        "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max"
        "&timezone=auto";

    final res = await http.get(Uri.parse(url));

    if (res.statusCode != 200) {
      throw Exception("Weather API failed");
    }

    final data = jsonDecode(res.body);
    final daily = data["daily"];

    List tmax = daily["temperature_2m_max"];
    List tmin = daily["temperature_2m_min"];
    List prcp = daily["precipitation_sum"];
    List wspd = daily["windspeed_10m_max"];

    double avgTmax = tmax.reduce((a, b) => a + b) / tmax.length;
    double avgTmin = tmin.reduce((a, b) => a + b) / tmin.length;
    double totalRain = prcp.reduce((a, b) => a + b);
    double avgWind = wspd.reduce((a, b) => a + b) / wspd.length;

    double tavg = (avgTmax + avgTmin) / 2;

    return {
      "tavg": tavg,
      "tmin": avgTmin,
      "tmax": avgTmax,
      "prcp": totalRain, // 🔥 WEEKLY rainfall
      "wspd": avgWind,
    };
  }
}