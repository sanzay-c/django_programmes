part of 'home_bloc.dart';

@immutable
abstract class HomeState {}

class HomeInitialState extends HomeState {}

class HomeLoadingState extends HomeState {}

class HomeSuccessState extends HomeState {
  final List<PersonsModel> personsData;

  HomeSuccessState({required this.personsData});
}

class HomeErrorState extends HomeState {
  final String error;

  HomeErrorState({required this.error});
}