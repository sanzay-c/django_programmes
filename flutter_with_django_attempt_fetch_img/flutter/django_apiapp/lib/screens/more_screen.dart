import 'package:flutter/material.dart';
import 'package:django_apiapp/services/api_services.dart';

class MoreScreen extends StatefulWidget {
  final int personId;

  const MoreScreen({super.key, required this.personId});

  @override
  State<MoreScreen> createState() => _MoreScreenState();
}

class _MoreScreenState extends State<MoreScreen> {
  double _elevation = 4.0;  // Initial elevation for the Card

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Detail Screen'),
        centerTitle: true,
      ),
      body: FutureBuilder(
        future: fetchPersonDetails(widget.personId),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('${snapshot.error}'));
          } else if (snapshot.hasData) {
            final person = snapshot.data!;
            return Padding(
              padding: const EdgeInsets.all(16.0),
              child: InkWell(
                onTap: () {
                  setState(() {
                    // Toggle the elevation on tap
                    _elevation = _elevation == 4.0 ? 8.0 : 4.0;
                  });
                },
                child: Card(
                  shape: RoundedRectangleBorder(
                    side: BorderSide(
                      color: const Color.fromARGB(94, 6, 6, 6),
                      width: 1.5,
                    ),
                    borderRadius: BorderRadius.circular(15),
                  ),
                  child: Container(
                    width: double.infinity,
                    child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          ClipOval(
                            child: Image.network(
                              person.profilePic,
                              width: 100.0,
                              height: 100.0,
                              fit: BoxFit.cover,
                            ),
                          ),
                          SizedBox(height: 10),
                          Text(
                            person.name,
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 5),
                          Text(
                            "Person ID: ${person.id}",
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            );
          }
          return SizedBox(); // Handle empty data or no data
        },
      ),
    );
  }
}
