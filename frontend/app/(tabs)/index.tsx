import React, { useCallback, useState } from "react";
import {
  ActivityIndicator,
  ImageBackground,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import Animated, { FadeIn } from "react-native-reanimated";

import { Colors, Fonts, Images, Radius, Spacing } from "@/constants/theme";
import { GameSelector } from "@/src/components/GameSelector";
import { LotteryBall } from "@/src/components/LotteryBall";
import { getGame, GameKey } from "@/src/data/games";
import { api, DrawResult } from "@/src/lib/api";

export default function GeneratorScreen() {
  const insets = useSafeAreaInsets();
  const [game, setGame] = useState<GameKey>("EJ");
  const [result, setResult] = useState<DrawResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const cfg = getGame(game);

  const onSelect = (key: GameKey) => {
    setGame(key);
    setResult(null);
    setError(null);
  };

  const generate = useCallback(async () => {
    if (Platform.OS !== "web") Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    setLoading(true);
    setError(null);
    try {
      const r = await api.drawQuantum(game);
      setResult(r);
    } catch (e: any) {
      setError(e?.message ?? "Quantum-Verbindung fehlgeschlagen");
    } finally {
      setLoading(false);
    }
  }, [game]);

  return (
    <View style={styles.container}>
      <ImageBackground
        source={{ uri: Images.heroBackground }}
        style={[styles.hero, { paddingTop: insets.top + Spacing.md }]}
      >
        <LinearGradient
          colors={["rgba(2,6,23,0.45)", "rgba(2,6,23,0.95)"]}
          style={StyleSheet.absoluteFill}
        />
        <Text style={styles.brand} allowFontScaling={false}>
          VORTEX
        </Text>
        <Text style={styles.tagline} allowFontScaling={false}>
          Quanten-Lotto · Global Karma 2026
        </Text>
      </ImageBackground>

      <View style={styles.selectorWrap}>
        <GameSelector selected={game} onSelect={onSelect} />
      </View>

      <ScrollView
        contentContainerStyle={styles.scroll}
        showsVerticalScrollIndicator={false}
      >
        <Text style={[styles.gameTitle, { color: cfg.color }]} allowFontScaling={false}>
          {cfg.name}
        </Text>

        {!result && !loading && !error && (
          <View style={styles.placeholder} testID="generator-placeholder">
            <Ionicons name="sparkles-outline" size={48} color={Colors.onSurfaceTertiary} />
            <Text style={styles.placeholderText}>
              Tippe auf „Quantum ziehen“, um deine Zahlen{"\n"}aus echtem Quanten-Zufall zu erzeugen.
            </Text>
          </View>
        )}

        {loading && (
          <View style={styles.placeholder} testID="generator-loading">
            <ActivityIndicator size="large" color={Colors.brand} />
            <Text style={styles.placeholderText}>Quanten werden gemessen…</Text>
          </View>
        )}

        {error && (
          <View style={styles.errorCard} testID="generator-error">
            <Ionicons name="warning-outline" size={28} color={Colors.error} />
            <Text style={styles.errorText}>{error}</Text>
            <Pressable style={styles.retryBtn} onPress={generate} testID="generator-retry">
              <Text style={styles.retryText}>Erneut versuchen</Text>
            </Pressable>
          </View>
        )}

        {result && (
          <Animated.View entering={FadeIn} testID="generator-result">
            <View style={styles.ballsRow}>
              {result.main.map((n, i) => (
                <LotteryBall
                  key={`${result.generated_at}-m-${i}`}
                  value={n}
                  color={cfg.color}
                  delay={i * 90}
                  pad={!cfg.digits}
                  testID={`ball-main-${i}`}
                />
              ))}
            </View>

            {result.extra.length > 0 && (
              <View style={styles.extraWrap}>
                <Text style={styles.extraLabel} allowFontScaling={false}>
                  {result.extraLabel ?? "Zusatz"}
                </Text>
                <View style={styles.ballsRow}>
                  {result.extra.map((n, i) => (
                    <LotteryBall
                      key={`${result.generated_at}-e-${i}`}
                      value={n}
                      color={Colors.warning}
                      delay={(result.main.length + i) * 90}
                      testID={`ball-extra-${i}`}
                    />
                  ))}
                </View>
              </View>
            )}

            <View
              style={[
                styles.sourceBadge,
                {
                  borderColor:
                    result.source === "quantum" ? Colors.brandSecondary : Colors.warning,
                },
              ]}
              testID="source-badge"
            >
              <Ionicons
                name={result.source === "quantum" ? "flash" : "shield-checkmark"}
                size={14}
                color={result.source === "quantum" ? Colors.brandSecondary : Colors.warning}
              />
              <Text
                style={[
                  styles.sourceText,
                  { color: result.source === "quantum" ? Colors.brandSecondary : Colors.warning },
                ]}
                allowFontScaling={false}
              >
                {result.source === "quantum"
                  ? "Echter Quanten-Zufall (ANU)"
                  : "Krypto-Zufall (Fallback)"}
              </Text>
            </View>
          </Animated.View>
        )}
      </ScrollView>

      <View style={[styles.ctaWrap, { paddingBottom: Spacing.md }]}>
        <Pressable
          testID="quantum-draw-button"
          onPress={generate}
          disabled={loading}
          style={({ pressed }) => [
            styles.cta,
            { backgroundColor: cfg.color, opacity: loading ? 0.6 : pressed ? 0.85 : 1 },
          ]}
        >
          <Ionicons name="sparkles" size={20} color={Colors.surface} />
          <Text style={styles.ctaText} allowFontScaling={false}>
            QUANTUM ZIEHEN
          </Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.surface },
  hero: {
    paddingHorizontal: Spacing.xl,
    paddingBottom: Spacing.lg,
  },
  brand: {
    fontFamily: Fonts.displayBold,
    fontSize: 40,
    color: Colors.brand,
    letterSpacing: 4,
  },
  tagline: {
    fontFamily: Fonts.bodyMedium,
    fontSize: 13,
    color: Colors.onSurfaceSecondary,
    marginTop: 2,
  },
  selectorWrap: {
    paddingVertical: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  scroll: {
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.lg,
    paddingBottom: Spacing.xl,
    alignItems: "center",
  },
  gameTitle: {
    fontFamily: Fonts.displayBold,
    fontSize: 22,
    letterSpacing: 1,
    marginBottom: Spacing.lg,
  },
  placeholder: {
    alignItems: "center",
    gap: Spacing.md,
    paddingVertical: Spacing.xxl,
  },
  placeholderText: {
    fontFamily: Fonts.body,
    fontSize: 14,
    color: Colors.onSurfaceTertiary,
    textAlign: "center",
    lineHeight: 20,
  },
  ballsRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: Spacing.md,
    justifyContent: "center",
  },
  extraWrap: {
    marginTop: Spacing.xl,
    alignItems: "center",
    gap: Spacing.sm,
  },
  extraLabel: {
    fontFamily: Fonts.displaySemi,
    fontSize: 13,
    color: Colors.onSurfaceTertiary,
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  sourceBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    alignSelf: "center",
    marginTop: Spacing.xl,
    paddingHorizontal: Spacing.md,
    paddingVertical: 6,
    borderRadius: Radius.pill,
    borderWidth: 1,
    backgroundColor: Colors.glassLight,
  },
  sourceText: { fontFamily: Fonts.bodyMedium, fontSize: 12 },
  errorCard: {
    alignItems: "center",
    gap: Spacing.md,
    backgroundColor: "rgba(244,63,94,0.12)",
    borderColor: Colors.error,
    borderWidth: 1,
    borderRadius: Radius.lg,
    padding: Spacing.xl,
    marginTop: Spacing.lg,
  },
  errorText: {
    fontFamily: Fonts.bodyMedium,
    color: Colors.onSurface,
    textAlign: "center",
  },
  retryBtn: {
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.sm,
    borderRadius: Radius.pill,
    backgroundColor: Colors.error,
  },
  retryText: { fontFamily: Fonts.displaySemi, color: Colors.onSurface },
  ctaWrap: {
    paddingHorizontal: Spacing.xl,
    paddingTop: Spacing.sm,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
    backgroundColor: Colors.surface,
  },
  cta: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: Spacing.sm,
    height: 58,
    borderRadius: Radius.lg,
  },
  ctaText: {
    fontFamily: Fonts.displayBold,
    fontSize: 20,
    color: Colors.surface,
    letterSpacing: 2,
  },
});
