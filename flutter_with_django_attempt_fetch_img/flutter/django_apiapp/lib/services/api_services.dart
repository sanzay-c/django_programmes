import 'dart:convert';
import 'package:django_apiapp/models/persons_model.dart';
import 'package:http/http.dart' as http;

Future<List<PersonsModel>> fetchData() async {
  try {
    const baseUrl = 'http://10.0.2.2:8000/api/persons/';
    final response = await http.get(Uri.parse(baseUrl));
    if (response.statusCode == 200) {
      List<dynamic> jsonData = json.decode(response.body);
      List<PersonsModel> fetchList =
          jsonData.map((item) => PersonsModel.fromJson(item)).toList();

      print(response.body);
      return fetchList;
    } else {
      throw Exception("Failed to Load Data");
    }
  } catch (e) {
    throw Exception("Error: $e");
  }
}

// api_services.dart
Future<PersonsModel> fetchPersonDetails(int personId) async {
  final response = await http.get(Uri.parse('http://10.0.2.2:8000/api/persons/$personId/'));
  if (response.statusCode == 200) {
    return PersonsModel.fromJson(json.decode(response.body));
  } else {
    throw Exception("Failed to load person details");
  }
}

