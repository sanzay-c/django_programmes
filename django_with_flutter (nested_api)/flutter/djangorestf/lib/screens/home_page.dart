import 'package:djangorestf/models/drf_model.dart';
import 'package:djangorestf/services/drf_services.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<DrfModel> drfModelBlog;

  ApiServices apiServices = ApiServices();

  // Function to refresh the data
  Future<void> _onRefresh(BuildContext context) async {
    // Triggering a refresh by reloading the data
    await apiServices.fetchData();
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("DRF Model List"),
        centerTitle: true,
      ),
      body: FutureBuilder(
        future: apiServices.fetchData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Text('${snapshot.error}'),
            );
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Text('No data available'),
            );
          } else {
            final List<DrfModel> model = snapshot.data!;
            return RefreshIndicator(
              onRefresh: () => _onRefresh(context),
              child: ListView.builder(
                itemCount: model.length,
                itemBuilder: (context, index) {
                  final drfList = model[index];
                  return Padding(
                    padding: const EdgeInsets.all(6.0),
                    child: Card(
                      elevation: 10,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              drfList.title,
                              style: const TextStyle(
                                fontSize: 24, 
                                fontWeight: FontWeight.bold,
                                color: Color(0xFFFE724C)
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              drfList.content,
                              style: const TextStyle(
                                fontSize: 16,
                                color: Colors.black87,
                              ),
                            ),
                            const SizedBox(height: 16),
                            Text(
                              'Comments:',
                              style: const TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Color.fromARGB(196, 254, 115, 76)
                              ),
                            ),
                            const SizedBox(height: 8),
                            // Display the comments for this model
                            for (var comment in drfList.comment)
                              Padding(
                                padding: const EdgeInsets.only(bottom: 12.0),
                                child: Card(
                                  elevation: 8,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Padding(
                                    padding: const EdgeInsets.all(12.0),
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          children: [
                                            CircleAvatar(
                                              child: Text(
                                                  comment.author[0].toUpperCase()),
                                              backgroundColor: Color(0xFFFE724C),
                                              foregroundColor: Colors.white,
                                            ),
                                            const SizedBox(width: 8),
                                            Text(
                                              comment.author,
                                              style: const TextStyle(
                                                fontWeight: FontWeight.bold,
                                                fontSize: 16,
                                              ),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          comment.content,
                                          style: const TextStyle(
                                            fontSize: 16,
                                            color: Colors.black87,
                                          ),
                                        ),
                                        const SizedBox(height: 8),
                                        Text(
                                          "Posted on: ${comment.createdAt.toLocal().toString().split(' ')[0]}",
                                          style: const TextStyle(
                                            fontSize: 12,
                                            fontWeight: FontWeight.bold,
                                            color: Color(0xFFFE724C),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              ),
            );
          }
        },
      ),
    );
  }
}
