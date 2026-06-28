import React, { useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  ImageBackground,
  Modal,
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
import * as WebBrowser from "expo-web-browser";
import * as Haptics from "expo-haptics";

import { Colors, Fonts, Images, Radius, Spacing } from "@/constants/theme";
import { api, CategoryGroup, ProjectItem, RandomKarma } from "@/src/lib/api";

const LABELS: Record<string, string> = {
  ALLE: "Alle",
  AUGSBURG: "Augsburg",
  BAYERN: "Bayern",
  DEUTSCHLAND: "Deutschland",
  SPANIEN: "Spanien",
  BOSNIEN: "Bosnien",
  GLOBAL: "Global",
  MEDIZIN: "Medizin",
  UMWELT: "Umwelt",
  COMMUNITY: "Community",
};

export default function KarmaScreen() {
  const insets = useSafeAreaInsets();
  const [groups, setGroups] = useState<CategoryGroup[]>([]);
  const [total, setTotal] = useState(0);
  const [active, setActive] = useState("ALLE");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [random, setRandom] = useState<RandomKarma | null>(null);
  const [randomLoading, setRandomLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);

  const load = async () => {
    setLoading(true);
    setError(false);
    try {
      const r = await api.getProjects();
      setGroups(r.categories);
      setTotal(r.total);
    } catch {
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const categories = useMemo(() => ["ALLE", ...groups.map((g) => g.category)], [groups]);

  const items: { project: ProjectItem; category: string }[] = useMemo(() => {
    if (active === "ALLE") {
      return groups.flatMap((g) => g.projects.map((p) => ({ project: p, category: g.category })));
    }
    const g = groups.find((x) => x.category === active);
    return g ? g.projects.map((p) => ({ project: p, category: g.category })) : [];
  }, [groups, active]);

  const open = async (url: string) => {
    if (Platform.OS !== "web") Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    try {
      if (Platform.OS === "web") {
        window.open(url, "_blank");
      } else {
        await WebBrowser.openBrowserAsync(url);
      }
    } catch {}
  };

  const pickRandom = async () => {
    if (Platform.OS !== "web") Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
    setModalOpen(true);
    setRandom(null);
    setRandomLoading(true);
    try {
      const r = await api.randomKarma(active);
      setRandom(r);
    } catch {
      setRandom(null);
    } finally {
      setRandomLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <ImageBackground
        source={{ uri: Images.karmaHero }}
        style={[styles.hero, { paddingTop: insets.top + Spacing.lg }]}
      >
        <LinearGradient
          colors={["rgba(2,6,23,0.35)", "rgba(2,6,23,0.92)"]}
          style={StyleSheet.absoluteFill}
        />
        <Text style={styles.title} allowFontScaling={false}>
          KARMA PROJEKTE
        </Text>
        <Text style={styles.subtitle} allowFontScaling={false}>
          {total} Organisationen, die deine Aufmerksamkeit verdienen
        </Text>
      </ImageBackground>

      <Pressable style={styles.randomBtn} onPress={pickRandom} testID="karma-random-button">
        <Ionicons name="sparkles" size={18} color={Colors.surface} />
        <Text style={styles.randomBtnText} allowFontScaling={false}>
          QUANTEN-ZUFALL: PROJEKT WÄHLEN
        </Text>
      </Pressable>

      <View style={styles.chipBar}>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.chipRow}
        >
          {categories.map((c) => {
            const isActive = c === active;
            return (
              <Pressable
                key={c}
                testID={`karma-chip-${c}`}
                onPress={() => {
                  if (Platform.OS !== "web") Haptics.selectionAsync();
                  setActive(c);
                }}
                style={[
                  styles.chip,
                  {
                    borderColor: isActive ? Colors.brand : Colors.border,
                    backgroundColor: isActive ? "rgba(34,211,238,0.18)" : Colors.glassLight,
                  },
                ]}
              >
                <Text
                  allowFontScaling={false}
                  style={[styles.chipText, { color: isActive ? Colors.brand : Colors.onSurfaceTertiary }]}
                >
                  {LABELS[c] ?? c}
                </Text>
              </Pressable>
            );
          })}
        </ScrollView>
      </View>

      {loading && (
        <View style={styles.center} testID="karma-loading">
          <ActivityIndicator size="large" color={Colors.brand} />
        </View>
      )}

      {error && !loading && (
        <View style={styles.center} testID="karma-error">
          <Ionicons name="cloud-offline-outline" size={44} color={Colors.error} />
          <Text style={styles.emptyText}>Projekte konnten nicht geladen werden.</Text>
          <Pressable style={styles.retryBtn} onPress={load} testID="karma-retry">
            <Text style={styles.retryText}>Erneut versuchen</Text>
          </Pressable>
        </View>
      )}

      {!loading && !error && (
        <FlatList
          data={items}
          keyExtractor={(it, i) => `${it.category}-${it.project.name}-${i}`}
          contentContainerStyle={styles.list}
          showsVerticalScrollIndicator={false}
          renderItem={({ item }) => (
            <Pressable
              style={styles.projectCard}
              onPress={() => open(item.project.url)}
              testID={`project-${item.project.name}`}
            >
              <View style={styles.projectLeft}>
                <Text style={styles.projectName} allowFontScaling={false} numberOfLines={2}>
                  {item.project.name}
                </Text>
                <View style={styles.badge}>
                  <Text style={styles.badgeText} allowFontScaling={false}>
                    {LABELS[item.category] ?? item.category}
                  </Text>
                </View>
              </View>
              <Ionicons name="open-outline" size={22} color={Colors.brand} />
            </Pressable>
          )}
          ListEmptyComponent={
            <View style={styles.center} testID="karma-empty">
              <Ionicons name="earth-outline" size={44} color={Colors.onSurfaceTertiary} />
              <Text style={styles.emptyText}>Keine Projekte in dieser Kategorie gefunden.</Text>
            </View>
          }
        />
      )}

      <Modal
        visible={modalOpen}
        transparent
        animationType="fade"
        onRequestClose={() => setModalOpen(false)}
      >
        <Pressable style={styles.modalOverlay} onPress={() => setModalOpen(false)}>
          <Pressable style={styles.modalCard} onPress={() => {}} testID="karma-random-modal">
            <Pressable
              style={styles.modalClose}
              onPress={() => setModalOpen(false)}
              hitSlop={12}
              testID="karma-random-close"
            >
              <Ionicons name="close" size={24} color={Colors.onSurfaceTertiary} />
            </Pressable>

            <Ionicons name="sparkles" size={32} color={Colors.brand} />
            <Text style={styles.modalKicker} allowFontScaling={false}>
              QUANTEN-AUSWAHL
            </Text>

            {randomLoading && (
              <View style={styles.modalBody} testID="karma-random-loading">
                <ActivityIndicator size="large" color={Colors.brand} />
                <Text style={styles.modalHint}>Universum wird befragt…</Text>
              </View>
            )}

            {!randomLoading && random && (
              <View style={styles.modalBody} testID="karma-random-result">
                <View style={styles.badge}>
                  <Text style={styles.badgeText} allowFontScaling={false}>
                    {LABELS[random.category] ?? random.category}
                  </Text>
                </View>
                <Text style={styles.modalProject} allowFontScaling={false}>
                  {random.project.name}
                </Text>
                <Text style={styles.modalHint}>
                  Gleichverteilt aus {random.poolSize} Projekten ·{" "}
                  {random.source === "quantum" ? "Quanten-Zufall" : "Krypto-Zufall"}
                </Text>

                <Pressable
                  style={styles.modalPrimary}
                  onPress={() => open(random.project.url)}
                  testID="karma-random-open"
                >
                  <Ionicons name="open-outline" size={18} color={Colors.surface} />
                  <Text style={styles.modalPrimaryText} allowFontScaling={false}>
                    Projekt öffnen
                  </Text>
                </Pressable>
                <Pressable style={styles.modalSecondary} onPress={pickRandom} testID="karma-random-again">
                  <Ionicons name="shuffle" size={18} color={Colors.brand} />
                  <Text style={styles.modalSecondaryText} allowFontScaling={false}>
                    Nochmal ziehen
                  </Text>
                </Pressable>
              </View>
            )}

            {!randomLoading && !random && (
              <View style={styles.modalBody}>
                <Text style={styles.modalHint}>Auswahl fehlgeschlagen.</Text>
                <Pressable style={styles.modalSecondary} onPress={pickRandom}>
                  <Text style={styles.modalSecondaryText} allowFontScaling={false}>
                    Erneut versuchen
                  </Text>
                </Pressable>
              </View>
            )}
          </Pressable>
        </Pressable>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.surface },
  hero: { paddingHorizontal: Spacing.xl, paddingBottom: Spacing.lg },
  title: {
    fontFamily: Fonts.displayBold,
    fontSize: 30,
    color: Colors.onSurface,
    letterSpacing: 1.5,
  },
  subtitle: { fontFamily: Fonts.body, fontSize: 13, color: Colors.onSurfaceSecondary, marginTop: 2 },
  chipBar: {
    paddingVertical: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
    backgroundColor: Colors.surface,
  },
  chipRow: { gap: Spacing.sm, paddingHorizontal: Spacing.lg, alignItems: "center" },
  chip: {
    height: 36,
    paddingHorizontal: Spacing.lg,
    borderRadius: Radius.pill,
    borderWidth: 1.5,
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  chipText: { fontFamily: Fonts.displaySemi, fontSize: 14, letterSpacing: 0.4 },
  list: { padding: Spacing.lg, paddingBottom: Spacing.xxl, gap: Spacing.md },
  projectCard: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    backgroundColor: Colors.surfaceSecondary,
    borderRadius: Radius.lg,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.lg,
    gap: Spacing.md,
  },
  projectLeft: { flex: 1, gap: Spacing.sm },
  projectName: { fontFamily: Fonts.bodySemi, fontSize: 16, color: Colors.onSurface },
  badge: {
    alignSelf: "flex-start",
    paddingHorizontal: Spacing.sm,
    paddingVertical: 3,
    borderRadius: Radius.sm,
    backgroundColor: Colors.surfaceTertiary,
  },
  badgeText: {
    fontFamily: Fonts.displayMedium,
    fontSize: 11,
    color: Colors.onSurfaceTertiary,
    letterSpacing: 0.6,
    textTransform: "uppercase",
  },
  center: { flex: 1, alignItems: "center", justifyContent: "center", gap: Spacing.md, padding: Spacing.xl },
  emptyText: {
    fontFamily: Fonts.body,
    fontSize: 14,
    color: Colors.onSurfaceTertiary,
    textAlign: "center",
  },
  retryBtn: {
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.sm,
    borderRadius: Radius.pill,
    backgroundColor: Colors.brand,
  },
  retryText: { fontFamily: Fonts.displaySemi, color: Colors.surface },
  randomBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: Spacing.sm,
    marginHorizontal: Spacing.lg,
    marginTop: Spacing.md,
    height: 50,
    borderRadius: Radius.lg,
    backgroundColor: Colors.brand,
  },
  randomBtnText: {
    fontFamily: Fonts.displayBold,
    fontSize: 16,
    color: Colors.surface,
    letterSpacing: 1,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(2,6,23,0.85)",
    alignItems: "center",
    justifyContent: "center",
    padding: Spacing.xl,
  },
  modalCard: {
    width: "100%",
    maxWidth: 420,
    backgroundColor: Colors.surfaceSecondary,
    borderRadius: Radius.lg,
    borderWidth: 1,
    borderColor: Colors.borderStrong,
    padding: Spacing.xl,
    alignItems: "center",
    gap: Spacing.sm,
  },
  modalClose: { position: "absolute", top: Spacing.md, right: Spacing.md, padding: 4 },
  modalKicker: {
    fontFamily: Fonts.displaySemi,
    fontSize: 13,
    color: Colors.brand,
    letterSpacing: 2,
  },
  modalBody: { alignItems: "center", gap: Spacing.md, width: "100%", marginTop: Spacing.sm },
  modalProject: {
    fontFamily: Fonts.displayBold,
    fontSize: 26,
    color: Colors.onSurface,
    textAlign: "center",
    lineHeight: 30,
  },
  modalHint: {
    fontFamily: Fonts.body,
    fontSize: 13,
    color: Colors.onSurfaceTertiary,
    textAlign: "center",
  },
  modalPrimary: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: Spacing.sm,
    width: "100%",
    height: 50,
    borderRadius: Radius.md,
    backgroundColor: Colors.brand,
    marginTop: Spacing.sm,
  },
  modalPrimaryText: { fontFamily: Fonts.displaySemi, fontSize: 16, color: Colors.surface },
  modalSecondary: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: Spacing.sm,
    width: "100%",
    height: 50,
    borderRadius: Radius.md,
    borderWidth: 1,
    borderColor: Colors.brand,
  },
  modalSecondaryText: { fontFamily: Fonts.displaySemi, fontSize: 16, color: Colors.brand },
});
