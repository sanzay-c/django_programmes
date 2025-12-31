import 'package:django_apiapp/bloc/home_bloc.dart';
import 'package:django_apiapp/models/persons_model.dart';
import 'package:django_apiapp/screens/more_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Some Api data"),
        centerTitle: true,
      ),
      body: BlocProvider(
        //-- In Dart, the .. operator is called the cascade operator.
        //   It allows you to perform multiple operations on the same object 
        //   without needing to repeat the object reference. 
        //   this .. operator, It creates the object and calls the add() method on it right away.
        //   Without the cascade operator (..), you’d have to write it in two steps:
        //   ** HomeBloc bloc = HomeBloc();
        //      bloc.add(FetchPersonDataEvent()); ** --
        create: (context) => HomeBloc()..add(FetchPersonDataEvent()),
        child: BlocBuilder<HomeBloc, HomeState>(
          builder: (context, state) {
            if (state is HomeLoadingState) {
              return Center(child: CircularProgressIndicator());
            } else if (state is HomeErrorState) {
              return Center(child: Text(state.error));
            } else if (state is HomeSuccessState) {
              final List<PersonsModel> apidata = state.personsData;
              return ListView.builder(
                itemCount: apidata.length,
                itemBuilder: (context, index) {
                  final personData = apidata[index];
                  return Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Card(
                      child: Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 17, vertical: 17),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            CircleAvatar(
                              backgroundImage: NetworkImage(personData.profilePic),
                            ),
                            Column(
                              children: [
                                Text(
                                  personData.name,
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 18,
                                  ),
                                ),
                              ],
                            ),
                            GestureDetector(
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => MoreScreen(personId: personData.id),
                                  ),
                                );
                              },
                              child: Icon(Icons.more_horiz),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                },
              );
            }
            return Container();
          },
        ),
      ),
    );
  }
}
