import React, { useRef, useState } from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  Pressable,
  View,
} from 'react-native';
import quizBank from './quizData.json';

type Option = {
  text: string;
  correct: boolean;
  explanation: string;
};

type QuizQuestion = {
  question: string;
  options: Option[];
  ans?: number;
};

const sourceQuestions = quizBank as QuizQuestion[];

// Topic keywords for spacing — prevents consecutive questions on the same topic
const TOPIC_KEYWORDS: Record<string, string[]> = {
  voltage: ['voltage', 'volt', 'vdc', 'vac', 'impedance', 'ohm'],
  decibel: ['decibel', ' db ', ' db)', 'spl', 'gain', 'attenuation'],
  video: ['resolution', 'pixel', 'refresh', 'hdmi', 'display', 'fps', '4k', '1080'],
  network: ['network', 'tcp', 'udp', 'ip address', 'subnet', 'bandwidth', 'latency'],
  audio: ['frequency', 'hz', 'khz', 'amplifier', 'speaker', 'microphone', 'reverb'],
  signal: ['signal', 'noise', 'snr', 'crosstalk', 'shielding', 'interference'],
};

function getTopicKey(question: string): string {
  const lower = question.toLowerCase();
  for (const [topic, keywords] of Object.entries(TOPIC_KEYWORDS)) {
    if (keywords.some((kw) => lower.includes(kw))) return topic;
  }
  return 'other';
}

function shuffle<T>(items: T[]) {
  const arr = [...items];
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function cloneQuestions() {
  return sourceQuestions.map((q) => ({
    question: q.question,
    options: q.options.map((o) => ({ ...o })),
    ans: undefined,
  }));
}

const TOPIC_COOLDOWN = 8; // Don't repeat a topic within this many questions

export default function App() {
  const deckRef = useRef<QuizQuestion[]>([]);
  const currentRef = useRef<number>(-1);
  const historyRef = useRef<number[]>([]);
  const futureRef = useRef<number[]>([]);
  const remainingRef = useRef<number[]>([]);
  const recentTopicsRef = useRef<string[]>([]);

  const [started, setStarted] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [score, setScore] = useState(0);
  const [, forceRender] = useState(0);

  function rebuildPool() {
    remainingRef.current = Array.from({ length: deckRef.current.length }, (_, i) => i);
    if (currentRef.current !== -1) {
      remainingRef.current = remainingRef.current.filter((i) => i !== currentRef.current);
    }
    remainingRef.current = shuffle(remainingRef.current);
  }

  function pickRandomQuestion() {
    if (remainingRef.current.length === 0) {
      rebuildPool();
    }

    const recentTopics = new Set(recentTopicsRef.current.slice(-TOPIC_COOLDOWN));

    // Try to find a candidate whose topic isn't in the recent window
    let candidatePos = -1;
    const preferred = remainingRef.current.filter((idx) => {
      const topic = getTopicKey(deckRef.current[idx].question);
      return !recentTopics.has(topic) || topic === 'other';
    });

    let chosenIdx: number;
    if (preferred.length > 0) {
      // Pick randomly from preferred candidates
      chosenIdx = preferred[Math.floor(Math.random() * preferred.length)];
      candidatePos = remainingRef.current.indexOf(chosenIdx);
    } else {
      // Fallback: pick any (pool too small to avoid topic)
      candidatePos = Math.floor(Math.random() * remainingRef.current.length);
      chosenIdx = remainingRef.current[candidatePos];
    }

    remainingRef.current.splice(candidatePos, 1);

    // Update recent topics window
    recentTopicsRef.current.push(getTopicKey(deckRef.current[chosenIdx].question));
    if (recentTopicsRef.current.length > 10) recentTopicsRef.current.shift();

    return chosenIdx;
  }

  function startQuiz() {
    const deck = cloneQuestions();
    deck.forEach((q) => {
      q.options = shuffle(q.options);
    });
    deckRef.current = deck;
    historyRef.current = [];
    futureRef.current = [];
    recentTopicsRef.current = [];
    remainingRef.current = Array.from({ length: deck.length }, (_, i) => i);
    remainingRef.current = shuffle(remainingRef.current);
    currentRef.current = pickRandomQuestion();
    setScore(0);
    setCurrentIndex(currentRef.current);
    setStarted(true);
    forceRender((v) => v + 1);
  }

  function goNext() {
    if (!started) return;

    if (futureRef.current.length > 0) {
      historyRef.current.push(currentRef.current);
      currentRef.current = futureRef.current.pop() as number;
      setCurrentIndex(currentRef.current);
      forceRender((v) => v + 1);
      return;
    }

    if (currentRef.current !== -1) {
      historyRef.current.push(currentRef.current);
    }

    const next = pickRandomQuestion();
    currentRef.current = next;
    setCurrentIndex(next);
    forceRender((v) => v + 1);
  }

  function goPrev() {
    if (!started || historyRef.current.length === 0) return;
    futureRef.current.push(currentRef.current);
    currentRef.current = historyRef.current.pop() as number;
    setCurrentIndex(currentRef.current);
    forceRender((v) => v + 1);
  }

  function answerQuestion(optionIndex: number) {
    const q = deckRef.current[currentIndex];
    if (!q || q.ans !== undefined) return;

    q.ans = optionIndex;
    if (q.options[optionIndex]?.correct) {
      setScore((s) => s + 1);
    }
    forceRender((v) => v + 1);
  }

  const currentQuestion = started && currentIndex >= 0 ? deckRef.current[currentIndex] : null;
  const position = historyRef.current.length + 1;
  const total = deckRef.current.length || sourceQuestions.length;

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar barStyle="light-content" />
      <View style={styles.screen}>
        {!started ? (
          <View style={styles.startOverlay}>
            <Text style={styles.title}>CTS Mastery</Text>
            <Text style={styles.subtitle}>500 Technical Questions</Text>
            <Pressable onPress={startQuiz} style={styles.primaryButton}>
              <Text style={styles.primaryButtonText}>START STUDYING</Text>
            </Pressable>
          </View>
        ) : (
          <>
            <View style={styles.progressTrack}>
              <View style={[styles.progressFill, { width: `${Math.min(100, (position / total) * 100)}%` }]} />
            </View>
            <Text style={styles.stat}>
              SCORE: {score} | Q {position}/{total}
            </Text>

            <ScrollView contentContainerStyle={styles.card} showsVerticalScrollIndicator={false}>
              <Text style={styles.questionText}>{currentQuestion?.question ?? 'Loading...'}</Text>
              <View style={styles.optionList}>
                {currentQuestion?.options.map((option, index) => {
                  const isCorrect = option.correct;
                  const isChosen = currentQuestion.ans === index;
                  const showCorrect = currentQuestion.ans !== undefined && isCorrect;
                  const showWrong = currentQuestion.ans !== undefined && isChosen && !isCorrect;

                  return (
                    <Pressable
                      key={`${currentIndex}-${index}`}
                      onPress={() => answerQuestion(index)}
                      style={[
                        styles.option,
                        showCorrect && styles.optionCorrect,
                        showWrong && styles.optionWrong,
                      ]}
                    >
                      <Text style={styles.optionText}>{option.text}</Text>
                    </Pressable>
                  );
                })}
              </View>

              {currentQuestion?.ans !== undefined && !currentQuestion.options[currentQuestion.ans]?.correct ? (
                <View style={styles.feedbackBox}>
                  <Text style={styles.feedbackText}>
                    Incorrect. {currentQuestion.options[currentQuestion.ans]?.explanation || ''}
                  </Text>
                </View>
              ) : null}
            </ScrollView>

            <View style={styles.navRow}>
              <Pressable onPress={goPrev} style={[styles.navButton, styles.navButtonSecondary, historyRef.current.length === 0 && styles.disabled]}>
                <Text style={styles.navButtonText}>PREV</Text>
              </Pressable>
              <Pressable onPress={goNext} style={styles.navButton}>
                <Text style={styles.navButtonText}>NEXT</Text>
              </Pressable>
            </View>
          </>
        )}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  screen: {
    flex: 1,
    backgroundColor: '#0f172a',
    paddingHorizontal: 16,
    paddingTop: 12,
    paddingBottom: 12,
  },
  startOverlay: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    gap: 10,
  },
  title: {
    color: '#f8fafc',
    fontSize: 44,
    fontWeight: '800',
    textAlign: 'center',
    letterSpacing: 0.4,
  },
  subtitle: {
    color: '#94a3b8',
    fontSize: 18,
    marginBottom: 18,
  },
  primaryButton: {
    backgroundColor: '#06b6d4',
    paddingHorizontal: 26,
    paddingVertical: 18,
    borderRadius: 18,
    minWidth: 220,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  progressTrack: {
    height: 4,
    borderRadius: 999,
    backgroundColor: '#334155',
    overflow: 'hidden',
    marginBottom: 16,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#06b6d4',
  },
  stat: {
    color: '#94a3b8',
    textAlign: 'center',
    fontSize: 13,
    marginBottom: 12,
    letterSpacing: 0.3,
  },
  card: {
    backgroundColor: '#1e293b',
    borderRadius: 24,
    padding: 18,
    gap: 14,
  },
  questionText: {
    color: '#f8fafc',
    fontSize: 22,
    lineHeight: 30,
    fontWeight: '700',
  },
  optionList: {
    gap: 12,
  },
  option: {
    backgroundColor: '#334155',
    borderRadius: 16,
    paddingVertical: 16,
    paddingHorizontal: 16,
  },
  optionCorrect: {
    backgroundColor: '#22c55e',
  },
  optionWrong: {
    backgroundColor: '#ef4444',
  },
  optionText: {
    color: '#fff',
    fontSize: 16,
    lineHeight: 23,
    fontWeight: '600',
  },
  feedbackBox: {
    borderLeftWidth: 4,
    borderLeftColor: '#ef4444',
    backgroundColor: 'rgba(255,255,255,0.05)',
    borderRadius: 12,
    padding: 14,
  },
  feedbackText: {
    color: '#f8fafc',
    fontSize: 14,
    lineHeight: 20,
  },
  navRow: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 14,
  },
  navButton: {
    flex: 1,
    backgroundColor: '#06b6d4',
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: 'center',
  },
  navButtonSecondary: {
    backgroundColor: '#475569',
  },
  navButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '800',
    letterSpacing: 0.4,
  },
  disabled: {
    opacity: 0.35,
  },
});
