import { Stack } from "expo-router";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import { LogBox, View } from "react-native";
import { useFonts } from "expo-font";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";

import { useIconFonts } from "@/src/hooks/use-icon-fonts";
import { Colors } from "@/constants/theme";

LogBox.ignoreAllLogs(true);

// Keep the native splash visible from cold start until icon fonts register.
SplashScreen.preventAutoHideAsync();

export default function RootLayout() {
  const [iconsLoaded, iconsError] = useIconFonts();
  const [appFontsLoaded, appFontsError] = useFonts({
    "Rajdhani-Medium": require("@/assets/fonts/Rajdhani-Medium.ttf"),
    "Rajdhani-SemiBold": require("@/assets/fonts/Rajdhani-SemiBold.ttf"),
    "Rajdhani-Bold": require("@/assets/fonts/Rajdhani-Bold.ttf"),
    "IBMPlexSans-Regular": require("@/assets/fonts/IBMPlexSans-Regular.ttf"),
    "IBMPlexSans-Medium": require("@/assets/fonts/IBMPlexSans-Medium.ttf"),
    "IBMPlexSans-SemiBold": require("@/assets/fonts/IBMPlexSans-SemiBold.ttf"),
  });

  const ready = (iconsLoaded || iconsError) && (appFontsLoaded || appFontsError);

  useEffect(() => {
    if (ready) SplashScreen.hideAsync();
  }, [ready]);

  if (!ready) return null;

  return (
    <GestureHandlerRootView style={{ flex: 1, backgroundColor: Colors.surface }}>
      <SafeAreaProvider>
        <StatusBar style="light" />
        <View style={{ flex: 1, backgroundColor: Colors.surface }}>
          <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: Colors.surface } }} />
        </View>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
