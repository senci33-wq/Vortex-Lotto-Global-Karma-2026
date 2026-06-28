import React from "react";
import { Pressable, ScrollView, StyleSheet, Text } from "react-native";
import * as Haptics from "expo-haptics";
import { Platform } from "react-native";

import { Colors, Fonts, Radius, Spacing } from "@/constants/theme";
import { GAMES, GameKey } from "@/src/data/games";

interface Props {
  selected: GameKey;
  onSelect: (key: GameKey) => void;
}

export function GameSelector({ selected, onSelect }: Props) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.row}
      style={styles.scroller}
    >
      {GAMES.map((g) => {
        const active = g.key === selected;
        return (
          <Pressable
            key={g.key}
            testID={`game-chip-${g.key}`}
            onPress={() => {
              if (Platform.OS !== "web") Haptics.selectionAsync();
              onSelect(g.key);
            }}
            style={[
              styles.chip,
              {
                borderColor: active ? g.color : Colors.border,
                backgroundColor: active ? `${g.color}26` : Colors.glassLight,
              },
            ]}
          >
            <Text
              allowFontScaling={false}
              style={[
                styles.chipText,
                { color: active ? g.color : Colors.onSurfaceTertiary },
              ]}
            >
              {g.name}
            </Text>
          </Pressable>
        );
      })}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroller: { flexGrow: 0 },
  row: {
    gap: Spacing.sm,
    paddingHorizontal: Spacing.lg,
    alignItems: "center",
  },
  chip: {
    height: 40,
    paddingHorizontal: Spacing.lg,
    borderRadius: Radius.pill,
    borderWidth: 1.5,
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  chipText: {
    fontFamily: Fonts.displaySemi,
    fontSize: 15,
    letterSpacing: 0.5,
  },
});
