import React from "react";
import { StyleSheet, Text, View } from "react-native";
import Animated, { FadeIn, ZoomIn } from "react-native-reanimated";

import { Colors, Fonts } from "@/constants/theme";

interface Props {
  value: number;
  color: string;
  size?: number;
  delay?: number;
  pad?: boolean;
  testID?: string;
}

export function LotteryBall({
  value,
  color,
  size = 54,
  delay = 0,
  pad = true,
  testID,
}: Props) {
  const label = pad ? String(value).padStart(2, "0") : String(value);
  return (
    <Animated.View
      entering={ZoomIn.delay(delay).springify().damping(12)}
      testID={testID}
      style={[
        styles.ball,
        {
          width: size,
          height: size,
          borderRadius: size / 2,
          borderColor: color,
          backgroundColor: `${color}26`,
          shadowColor: color,
        },
      ]}
    >
      <Text
        style={[styles.text, { color, fontSize: size * 0.42 }]}
        allowFontScaling={false}
      >
        {label}
      </Text>
    </Animated.View>
  );
}

export function StaticBall({
  value,
  color,
  size = 34,
  pad = true,
}: {
  value: number;
  color: string;
  size?: number;
  pad?: boolean;
}) {
  const label = pad ? String(value).padStart(2, "0") : String(value);
  return (
    <View
      style={[
        styles.ball,
        {
          width: size,
          height: size,
          borderRadius: size / 2,
          borderColor: color,
          backgroundColor: `${color}1f`,
          shadowOpacity: 0,
        },
      ]}
    >
      <Text style={[styles.text, { color, fontSize: size * 0.42 }]} allowFontScaling={false}>
        {label}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  ball: {
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1.5,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.7,
    shadowRadius: 10,
    elevation: 6,
  },
  text: {
    fontFamily: Fonts.displayBold,
    includeFontPadding: false,
    textShadowColor: Colors.surface,
    textShadowRadius: 2,
  },
});
