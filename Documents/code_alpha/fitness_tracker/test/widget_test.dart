import 'package:flutter_test/flutter_test.dart';

import 'package:fitness_tracker/main.dart';
import 'package:fitness_tracker/services/fitness_service.dart';

void main() {
  testWidgets('shows the fitness dashboard', (tester) async {
    await tester.pumpWidget(FitnessApp(service: FitnessService.preview()));
    await tester.pump();

    expect(find.text('Bonjour, Nadège 👋'), findsOneWidget);
    expect(find.text('Pas aujourd’hui'), findsOneWidget);
    expect(find.text('Cette semaine'), findsOneWidget);
  });
}
