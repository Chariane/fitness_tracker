import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'screens/dashboard_screen.dart';
import 'services/fitness_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final service = await FitnessService.connect();
  runApp(FitnessApp(service: service));
}

class FitnessApp extends StatelessWidget {
  const FitnessApp({required this.service, super.key});

  final FitnessService service;

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Pulse Fitness',
    debugShowCheckedModeBanner: false,
    locale: const Locale('fr'),
    supportedLocales: const [Locale('fr')],
    localizationsDelegates: GlobalMaterialLocalizations.delegates,
    theme: ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: const Color(0xFFF5F6F2),
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF164E3B),
        primary: const Color(0xFF164E3B),
        surface: Colors.white,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFFF5F6F2),
        foregroundColor: Color(0xFF17251E),
        elevation: 0,
      ),
    ),
    home: DashboardScreen(service: service),
  );
}
