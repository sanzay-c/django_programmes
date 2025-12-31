import 'dart:convert';

class PersonsModel {
  final int id;
  final String name;
  final String profilePic;

  PersonsModel({
    required this.id,
    required this.name,
    required this.profilePic,
  });

  // Factory method to parse a raw JSON string
  factory PersonsModel.fromRawJson(String str) => PersonsModel.fromJson(json.decode(str));

  // Convert the object back to JSON string
  String toRawJson() => json.encode(toJson());

  // Factory method to create an object from a map (parsed JSON)
  factory PersonsModel.fromJson(Map<String, dynamic> json) {
    return PersonsModel(
      id: json["id"], // Assuming ID is always present
      name: json["name"] ?? 'Unknown', // Default to 'Unknown' if name is null
      profilePic: json["profile_pic"] ?? '', // Default to empty string if profile_pic is null
    );
  }

  // Convert the object back to a map (JSON format)
  Map<String, dynamic> toJson() => {
    "id": id,
    "name": name,
    "profile_pic": profilePic,
  };
}
