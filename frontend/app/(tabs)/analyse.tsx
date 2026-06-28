import React, { useCallback, useEffect, useState } from "react";
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useFocusEffect } from "expo-router";
import { Ionicons } from "@expo/vector-icons";

import { Colors, Fonts, Radius, Spacing } from "@/constants/theme";
import { GameSelector } from "@/src/components/GameSelector";
import { StaticBall } from "@/src/components/LotteryBall";
import { getGame, GameKey } from "@/src/data/games";
import { api, AnalysisResult, Draw } from "@/src/lib/api";

export default function AnalyseScreen() {
  const insets = useSafeAreaInsets();
  const [game, setGame] = useState<GameKey>("EJ");
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [draws, setDraws] = useState<Draw[]>([]);
  const [loading, setLoading] = useState(true);
  const [input, setInput] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  const cfg = getGame(game);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [a, d] = await Promise.all([api.getAnalysis(game), api.listDraws(game)]);
      setAnalysis(a);
      setDraws(d);
    } catch {
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  }, [game]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  useEffect(() => {
    setMsg(null);
  }, [game]);

  const addDraw = async () => {
    const nums = input
      .split(/[\s,;|]+/)
      .map((x) => parseInt(x, 10))
      .filter((x) => !Number.isNaN(x));
    if (nums.length < cfg.mc) {
      setMsg(`Bitte mindestens ${cfg.mc} Zahlen eingeben.`);
      return;
    }
    try {
      await api.addDraw(game, nums.slice(0, cfg.mc), nums.slice(cfg.mc, cfg.mc + cfg.ec));
      setInput("");
      setMsg("Ziehung gespeichert!");
      load();
    } catch (e: any) {
      setMsg(e?.message ?? "Fehler beim Speichern");
    }
  };

  const remove = async (id: string) => {
    await api.deleteDraw(id);
    load();
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={[styles.header, { paddingTop: insets.top + Spacing.md }]}>
        <Text style={styles.title} allowFontScaling={false}>
          QUANTUM ANALYSE
        </Text>
        <Text style={styles.subtitle} allowFontScaling={false}>
          Häufigkeit deiner gespeicherten Ziehungen
        </Text>
      </View>

      <View style={styles.selectorWrap}>
        <GameSelector selected={game} onSelect={setGame} />
      </View>

      <ScrollView
        contentContainerStyle={styles.scroll}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        {/* Add draw */}
        <View style={styles.card}>
          <Text style={styles.cardLabel} allowFontScaling={false}>
            Vergangene Ziehung hinzufügen
          </Text>
          <View style={styles.inputRow}>
            <TextInput
              testID="draw-input"
              value={input}
              onChangeText={setInput}
              placeholder={`z.B. ${Array.from({ length: cfg.mc }, (_, i) => i + 1).join(" ")}`}
              placeholderTextColor={Colors.onSurfaceTertiary}
              keyboardType="numbers-and-punctuation"
              style={styles.input}
            />
            <Pressable style={[styles.addBtn, { backgroundColor: cfg.color }]} onPress={addDraw} testID="add-draw-button">
              <Ionicons name="add" size={26} color={Colors.surface} />
            </Pressable>
          </View>
          {msg && (
            <Text style={styles.msg} testID="draw-msg">
              {msg}
            </Text>
          )}
        </View>

        {loading && (
          <View style={styles.center} testID="analyse-loading">
            <ActivityIndicator color={Colors.brand} size="large" />
          </View>
        )}

        {!loading && analysis && analysis.totalDraws === 0 && (
          <View style={styles.center} testID="analyse-empty">
            <Ionicons name="grid-outline" size={44} color={Colors.onSurfaceTertiary} />
            <Text style={styles.emptyText}>
              Keine Ziehungen vorhanden.{"\n"}Füge oben eine hinzu.
            </Text>
          </View>
        )}

        {!loading && analysis && analysis.totalDraws > 0 && (
          <>
            <Text style={styles.sectionTitle} allowFontScaling={false}>
              HOT-ZAHLEN
            </Text>
            <View style={styles.card}>
              {analysis.hot.map((h) => (
                <View key={h.n} style={styles.barRow}>
                  <Text style={styles.barNum} allowFontScaling={false}>
                    {String(h.n).padStart(2, "0")}
                  </Text>
                  <View style={styles.barTrack}>
                    <View
                      style={[
                        styles.barFill,
                        {
                          width: `${analysis.max ? (h.count / analysis.max) * 100 : 0}%`,
                          backgroundColor: cfg.color,
                        },
                      ]}
                    />
                  </View>
                  <Text style={styles.barCount} allowFontScaling={false}>
                    {h.count}×
                  </Text>
                </View>
              ))}
            </View>

            <Text style={styles.sectionTitle} allowFontScaling={false}>
              ZIEHUNGEN ({analysis.totalDraws})
            </Text>
            {draws.map((d) => (
              <View key={d.id} style={styles.drawRow} testID={`draw-row-${d.id}`}>
                <View style={styles.drawBalls}>
                  {d.main.map((n, i) => (
                    <StaticBall key={i} value={n} color={cfg.color} pad={!cfg.digits} />
                  ))}
                  {d.extra.map((n, i) => (
                    <StaticBall key={`e${i}`} value={n} color={Colors.warning} />
                  ))}
                </View>
                <Pressable onPress={() => remove(d.id)} hitSlop={10} testID={`delete-draw-${d.id}`}>
                  <Ionicons name="trash-outline" size={20} color={Colors.error} />
                </Pressable>
              </View>
            ))}
          </>
        )}
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.surface },
  header: { paddingHorizontal: Spacing.xl, paddingBottom: Spacing.md },
  title: {
    fontFamily: Fonts.displayBold,
    fontSize: 28,
    color: Colors.onSurface,
    letterSpacing: 1.5,
  },
  subtitle: { fontFamily: Fonts.body, fontSize: 13, color: Colors.onSurfaceTertiary },
  selectorWrap: {
    paddingBottom: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  scroll: { padding: Spacing.xl, paddingBottom: Spacing.xxl, gap: Spacing.md },
  card: {
    backgroundColor: Colors.surfaceSecondary,
    borderRadius: Radius.lg,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.lg,
    gap: Spacing.md,
  },
  cardLabel: { fontFamily: Fonts.displaySemi, fontSize: 15, color: Colors.onSurfaceSecondary },
  inputRow: { flexDirection: "row", gap: Spacing.sm },
  input: {
    flex: 1,
    height: 48,
    borderRadius: Radius.md,
    backgroundColor: Colors.surfaceTertiary,
    borderWidth: 1,
    borderColor: Colors.border,
    paddingHorizontal: Spacing.md,
    color: Colors.onSurface,
    fontFamily: Fonts.bodyMedium,
    fontSize: 16,
  },
  addBtn: {
    width: 48,
    height: 48,
    borderRadius: Radius.md,
    alignItems: "center",
    justifyContent: "center",
  },
  msg: { fontFamily: Fonts.body, fontSize: 13, color: Colors.brandSecondary },
  center: { alignItems: "center", gap: Spacing.md, paddingVertical: Spacing.xxl },
  emptyText: {
    fontFamily: Fonts.body,
    fontSize: 14,
    color: Colors.onSurfaceTertiary,
    textAlign: "center",
    lineHeight: 20,
  },
  sectionTitle: {
    fontFamily: Fonts.displayBold,
    fontSize: 16,
    color: Colors.onSurfaceSecondary,
    letterSpacing: 1.5,
    marginTop: Spacing.sm,
  },
  barRow: { flexDirection: "row", alignItems: "center", gap: Spacing.md },
  barNum: {
    width: 28,
    fontFamily: Fonts.displayBold,
    fontSize: 16,
    color: Colors.onSurface,
  },
  barTrack: {
    flex: 1,
    height: 12,
    borderRadius: Radius.pill,
    backgroundColor: Colors.surfaceTertiary,
    overflow: "hidden",
  },
  barFill: { height: "100%", borderRadius: Radius.pill },
  barCount: {
    width: 36,
    textAlign: "right",
    fontFamily: Fonts.displayMedium,
    fontSize: 14,
    color: Colors.onSurfaceTertiary,
  },
  drawRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: Colors.surfaceSecondary,
    borderRadius: Radius.md,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
  },
  drawBalls: { flexDirection: "row", flexWrap: "wrap", gap: Spacing.xs, flex: 1 },
});
