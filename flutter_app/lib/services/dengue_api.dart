import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://10.0.2.2:5000";

  static Future<Map<String, dynamic>> predictRisk(
      Map<String, dynamic> payload) async {
    try {
      final response = await http
          .post(
            Uri.parse("$baseUrl/predict"),
            headers: {"Content-Type": "application/json"},
            body: jsonEncode(payload),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        print("API Response: $data"); // ✅ Debug

        return data;
      } else {
        throw Exception(
            "Server error: ${response.statusCode} - ${response.body}");
      }
    } catch (e) {
      throw Exception("API Error: $e");
    }
  }
}