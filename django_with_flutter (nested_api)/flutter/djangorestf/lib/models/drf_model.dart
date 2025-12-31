import 'dart:convert';

class DrfModel {
    int id;
    List<Comment> comment;
    String title;
    String content;

    DrfModel({
        required this.id,
        required this.comment,
        required this.title,
        required this.content,
    });

    factory DrfModel.fromRawJson(String str) => DrfModel.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory DrfModel.fromJson(Map<String, dynamic> json) => DrfModel(
        id: json["id"],
        comment: List<Comment>.from(json["comment"].map((x) => Comment.fromJson(x))),
        title: json["title"],
        content: json["content"],
    );

    Map<String, dynamic> toJson() => {
        "id": id,
        "comment": List<dynamic>.from(comment.map((x) => x.toJson())),
        "title": title,
        "content": content,
    };
}

class Comment {
    int id;
    String author;
    String content;
    DateTime createdAt;
    int blog;

    Comment({
        required this.id,
        required this.author,
        required this.content,
        required this.createdAt,
        required this.blog,
    });

    factory Comment.fromRawJson(String str) => Comment.fromJson(json.decode(str));

    String toRawJson() => json.encode(toJson());

    factory Comment.fromJson(Map<String, dynamic> json) => Comment(
        id: json["id"],
        author: json["author"],
        content: json["content"],
        createdAt: DateTime.parse(json["created_at"]),
        blog: json["blog"],
    );

    Map<String, dynamic> toJson() => {
        "id": id,
        "author": author,
        "content": content,
        "created_at": createdAt.toIso8601String(),
        "blog": blog,
    };
}
