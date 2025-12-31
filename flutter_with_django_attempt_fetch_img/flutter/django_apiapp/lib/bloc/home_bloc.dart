import 'package:bloc/bloc.dart';
import 'package:django_apiapp/models/persons_model.dart';
import 'package:django_apiapp/services/api_services.dart';
import 'package:meta/meta.dart';

part 'home_event.dart';
part 'home_state.dart';

class HomeBloc extends Bloc<HomeEvent, HomeState> {
  HomeBloc() : super(HomeInitialState()) {
    on<HomeInitialEvent>(_onHomeInitialEvent);
    on<FetchPersonDataEvent>(_onFetchPersonDataEvent);
  }

  Future<void> _onHomeInitialEvent(HomeInitialEvent event, Emitter<HomeState> emit) async {
    emit(HomeInitialState());
  }

  Future<void> _onFetchPersonDataEvent(FetchPersonDataEvent event, Emitter<HomeState> emit) async {
    emit(HomeLoadingState());
    try {
      final List<PersonsModel> persons = await fetchData();
      emit(HomeSuccessState(personsData: persons));
    } catch (e) {
      emit(HomeErrorState(error: e.toString()));
    }
  }
}
