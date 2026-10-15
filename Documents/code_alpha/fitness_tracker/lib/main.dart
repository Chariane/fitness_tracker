import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'screens/dashboard_screen.dart';
import 'services/fitness_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final service = await FitnessService.connect();
  final preferences = await SharedPreferences.getInstance();
  final initialDarkMode = preferences.getBool('fitness.dark_mode.v1') ?? false;
  runApp(FitnessApp(service: service, initialDarkMode: initialDarkMode));
}

class FitnessApp extends StatefulWidget {
  const FitnessApp({
    required this.service,
    this.initialDarkMode = false,
    super.key,
  });

  final FitnessService service;
  final bool initialDarkMode;

  @override
  State<FitnessApp> createState() => _FitnessAppState();
}

class _FitnessAppState extends State<FitnessApp> {
  late bool _isDark = widget.initialDarkMode;

  Future<void> _toggleTheme() async {
    final nextValue = !_isDark;
    setState(() => _isDark = nextValue);
    final preferences = await SharedPreferences.getInstance();
    await preferences.setBool('fitness.dark_mode.v1', nextValue);
  }

  ThemeData _buildTheme(Brightness brightness) {
    final isDark = brightness == Brightness.dark;
    final scheme = ColorScheme.fromSeed(
      seedColor: const Color(0xFF164E3B),
      brightness: brightness,
      primary: isDark ? const Color(0xFF91D5B3) : const Color(0xFF164E3B),
      surface: isDark ? const Color(0xFF121A16) : const Color(0xFFFFFFFF),
    );

    return ThemeData(
      useMaterial3: true,
      brightness: brightness,
      colorScheme: scheme,
      scaffoldBackgroundColor: isDark
          ? const Color(0xFF101713)
          : const Color(0xFFF5F6F2),
      appBarTheme: AppBarTheme(
        backgroundColor: isDark
            ? const Color(0xFF101713)
            : const Color(0xFFF5F6F2),
        foregroundColor: scheme.onSurface,
        elevation: 0,
        surfaceTintColor: Colors.transparent,
        scrolledUnderElevation: 0,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: scheme.surfaceContainerHighest,
        contentPadding: const EdgeInsets.symmetric(
          horizontal: 14,
          vertical: 15,
        ),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide(color: scheme.outlineVariant),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide(color: scheme.outlineVariant),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide(color: scheme.primary, width: 1.5),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: scheme.primary,
          foregroundColor: scheme.onPrimary,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15),
          ),
          textStyle: const TextStyle(fontWeight: FontWeight.w700),
        ),
      ),
      snackBarTheme: SnackBarThemeData(
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      ),
      bottomSheetTheme: BottomSheetThemeData(
        backgroundColor: scheme.surface,
        modalBackgroundColor: scheme.surface,
      ),
      dialogTheme: DialogThemeData(backgroundColor: scheme.surface),
    );
  }

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Pulse Fitness',
    debugShowCheckedModeBanner: false,
    locale: const Locale('fr'),
    supportedLocales: const [Locale('fr')],
    localizationsDelegates: GlobalMaterialLocalizations.delegates,
    theme: _buildTheme(Brightness.light),
    darkTheme: _buildTheme(Brightness.dark),
    themeMode: _isDark ? ThemeMode.dark : ThemeMode.light,
    home: DashboardScreen(
      service: widget.service,
      isDark: _isDark,
      onThemeToggle: _toggleTheme,
    ),
  );
}
