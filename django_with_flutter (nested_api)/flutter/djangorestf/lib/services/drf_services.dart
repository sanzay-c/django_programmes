import 'dart:convert';

import 'package:djangorestf/models/drf_model.dart';
import 'package:http/http.dart' as http;

class ApiServices {
  Future<List<DrfModel>> fetchData() async {
    try {
      const baseUrl = 'http://10.0.2.2:8000/api/blogs/';
      final response = await http.get(Uri.parse(baseUrl));
      if (response.statusCode == 200) {
        List<dynamic> jsonData = json.decode(response.body);
        List<DrfModel> fetchList =
            jsonData.map((e) => DrfModel.fromJson(e)).toList();
        print(response.body);
        return fetchList;
      } else {
        throw Exception("Failed to load data");
      }
    } catch (e) {
      throw Exception("Error occured $e");
    }
  }
}
