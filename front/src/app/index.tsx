import React, { useCallback, useEffect, useMemo, useState } from 'react'
import {
    ActivityIndicator,
    Alert,
    ScrollView,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View
} from 'react-native'
import { useSQLiteContext } from 'expo-sqlite'

type HabitRecord = {
    id: number
    name: string
}

const MAX_HABITS = 3
const POINT_INCREMENT = 10

const HomeScreen = (): JSX.Element => {
    const db = useSQLiteContext()
    const [habits, setHabits] = useState<HabitRecord[]>([])
    const [newHabitName, setNewHabitName] = useState('')
    const [editingHabit, setEditingHabit] = useState<HabitRecord | null>(null)
    const [totalPoints, setTotalPoints] = useState(0)
    const [errorMessage, setErrorMessage] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    const remainingSlots = useMemo(() => MAX_HABITS - habits.length, [habits.length])

    const loadHabits = useCallback(async () => {
        const result = await db.getAllAsync<HabitRecord>('SELECT id, name FROM habits ORDER BY id ASC')
        setHabits(result)
    }, [db])

    const loadPoints = useCallback(async () => {
        const row = await db.getFirstAsync<{ total: number }>('SELECT total FROM points WHERE id = 1')
        setTotalPoints(row?.total ?? 0)
    }, [db])

    useEffect(() => {
        let isMounted = true
        const initialize = async (): Promise<void> => {
            try {
                await loadHabits()
                await loadPoints()
            } catch (error) {
                console.error('Failed to load data from SQLite', error)
                if (isMounted) {
                    setErrorMessage('データの読み込みに失敗しました。アプリを再起動してください。')
                }
            } finally {
                if (isMounted) {
                    setIsLoading(false)
                }
            }
        }
        void initialize()
        return () => {
            isMounted = false
        }
    }, [loadHabits, loadPoints])

    const handleAddHabit = useCallback(async () => {
        const trimmedName = newHabitName.trim()
        if (!trimmedName) {
            setErrorMessage('習慣の内容を入力してください。')
            return
        }
        if (habits.length >= MAX_HABITS) {
            setErrorMessage('登録できる習慣は最大3つです。')
            return
        }
        try {
            await db.runAsync('INSERT INTO habits (name) VALUES (?)', [trimmedName])
            setNewHabitName('')
            setErrorMessage(null)
            await loadHabits()
        } catch (error) {
            console.error('Failed to add habit', error)
            setErrorMessage('習慣の追加に失敗しました。')
        }
    }, [db, habits.length, loadHabits, newHabitName])

    const handleStartEdit = useCallback((habit: HabitRecord) => {
        setEditingHabit(habit)
        setErrorMessage(null)
    }, [])

    const handleChangeEditingName = useCallback((text: string) => {
        setEditingHabit((prev) => (prev ? { ...prev, name: text } : prev))
    }, [])

    const handleSaveEdit = useCallback(async () => {
        if (!editingHabit) {
            return
        }
        const trimmedName = editingHabit.name.trim()
        if (!trimmedName) {
            setErrorMessage('習慣の内容を入力してください。')
            return
        }
        try {
            await db.runAsync('UPDATE habits SET name = ? WHERE id = ?', [trimmedName, editingHabit.id])
            setEditingHabit(null)
            setErrorMessage(null)
            await loadHabits()
        } catch (error) {
            console.error('Failed to update habit', error)
            setErrorMessage('習慣の更新に失敗しました。')
        }
    }, [db, editingHabit, loadHabits])

    const handleCancelEdit = useCallback(() => {
        setEditingHabit(null)
    }, [])

    const handleDeleteHabit = useCallback((habitId: number) => {
        Alert.alert('削除確認', 'この習慣を削除しますか？', [
            {
                text: 'キャンセル',
                style: 'cancel'
            },
            {
                text: '削除',
                style: 'destructive',
                onPress: () => {
                    void (async () => {
                        try {
                            await db.runAsync('DELETE FROM habits WHERE id = ?', [habitId])
                            if (editingHabit?.id === habitId) {
                                setEditingHabit(null)
                            }
                            setErrorMessage(null)
                            await loadHabits()
                        } catch (error) {
                            console.error('Failed to delete habit', error)
                            setErrorMessage('習慣の削除に失敗しました。')
                        }
                    })()
                }
            }
        ])
    }, [db, editingHabit, loadHabits])

    const handleCompleteHabit = useCallback(async () => {
        try {
            await db.runAsync('UPDATE points SET total = total + ? WHERE id = 1', [POINT_INCREMENT])
            await loadPoints()
        } catch (error) {
            console.error('Failed to update points', error)
            setErrorMessage('ポイントの更新に失敗しました。')
        }
    }, [db, loadPoints])

    const handleNewHabitNameChange = useCallback((text: string) => {
        setNewHabitName(text)
        if (errorMessage) {
            setErrorMessage(null)
        }
    }, [errorMessage])

    if (isLoading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#467FD3" />
                <Text style={styles.loadingText}>読み込み中...</Text>
            </View>
        )
    }

    return (
        <View style={styles.container}>
            <ScrollView contentContainerStyle={styles.scrollContent}>
                <View style={styles.pointsCard}>
                    <Text style={styles.pointsLabel}>現在の合計ポイント</Text>
                    <Text style={styles.pointsValue}>{totalPoints.toLocaleString()} pt</Text>
                    <Text style={styles.pointsDescription}>
                        習慣の達成ボタンを押すたびに{POINT_INCREMENT}ポイントが貯まります。
                    </Text>
                </View>

                <View style={styles.sectionHeader}>
                    <Text style={styles.sectionTitle}>登録した習慣</Text>
                    <Text style={styles.sectionSubtitle}>残り登録可能数: {remainingSlots} / {MAX_HABITS}</Text>
                </View>

                {habits.length === 0 ? (
                    <View style={styles.emptyState}>
                        <Text style={styles.emptyStateText}>まだ習慣が登録されていません。</Text>
                        <Text style={styles.emptyStateDescription}>下のフォームから習慣を登録してみましょう。</Text>
                    </View>
                ) : (
                    habits.map((habit, index) => (
                        <View key={habit.id} style={styles.habitCard}>
                            <View style={styles.habitHeader}>
                                <Text style={styles.habitIndex}>習慣 {index + 1}</Text>
                                <View style={styles.habitActions}>
                                    <TouchableOpacity
                                        style={[styles.actionButton, styles.editButton]}
                                        onPress={() => handleStartEdit(habit)}
                                    >
                                        <Text style={styles.actionButtonText}>編集</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        style={[styles.actionButton, styles.deleteButton]}
                                        onPress={() => handleDeleteHabit(habit.id)}
                                    >
                                        <Text style={styles.actionButtonText}>削除</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>

                            {editingHabit?.id === habit.id ? (
                                <View style={styles.editContainer}>
                                    <TextInput
                                        value={editingHabit.name}
                                        onChangeText={handleChangeEditingName}
                                        style={styles.input}
                                        placeholder="習慣の内容を入力"
                                        placeholderTextColor="#9CA3AF"
                                    />
                                    <View style={styles.editButtons}>
                                        <TouchableOpacity
                                            style={[styles.actionButton, styles.saveButton]}
                                            onPress={handleSaveEdit}
                                        >
                                            <Text style={styles.actionButtonText}>保存</Text>
                                        </TouchableOpacity>
                                        <TouchableOpacity
                                            style={[styles.actionButton, styles.cancelButton]}
                                            onPress={handleCancelEdit}
                                        >
                                            <Text style={styles.actionButtonText}>キャンセル</Text>
                                        </TouchableOpacity>
                                    </View>
                                </View>
                            ) : (
                                <Text style={styles.habitName}>{habit.name}</Text>
                            )}

                            <TouchableOpacity
                                style={styles.completeButton}
                                onPress={handleCompleteHabit}
                            >
                                <Text style={styles.completeButtonText}>{`達成！ (+${POINT_INCREMENT}pt)`}</Text>
                            </TouchableOpacity>
                        </View>
                    ))
                )}

                {habits.length < MAX_HABITS && (
                    <View style={styles.newHabitCard}>
                        <Text style={styles.sectionTitle}>新しい習慣を登録</Text>
                        <TextInput
                            value={newHabitName}
                            onChangeText={handleNewHabitNameChange}
                            style={styles.input}
                            placeholder="例: 毎朝ストレッチをする"
                            placeholderTextColor="#9CA3AF"
                        />
                        <TouchableOpacity
                            style={[styles.actionButton, styles.addButton]}
                            onPress={handleAddHabit}
                        >
                            <Text style={styles.actionButtonText}>追加する</Text>
                        </TouchableOpacity>
                    </View>
                )}

                {errorMessage && (
                    <View style={styles.errorContainer}>
                        <Text style={styles.errorText}>{errorMessage}</Text>
                    </View>
                )}
            </ScrollView>
        </View>
    )
}

export default HomeScreen

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F8F0E3'
    },
    scrollContent: {
        padding: 20,
        paddingBottom: 40
    },
    loadingContainer: {
        flex: 1,
        backgroundColor: '#F8F0E3',
        alignItems: 'center',
        justifyContent: 'center'
    },
    loadingText: {
        marginTop: 12,
        fontSize: 16,
        color: '#2C3E50',
        fontWeight: '600'
    },
    pointsCard: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 24,
        marginBottom: 24,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 6 },
        shadowOpacity: 0.1,
        shadowRadius: 10,
        elevation: 5
    },
    pointsLabel: {
        fontSize: 18,
        color: '#2C3E50',
        fontWeight: '700'
    },
    pointsValue: {
        fontSize: 48,
        fontWeight: '900',
        color: '#467FD3',
        marginTop: 10
    },
    pointsDescription: {
        marginTop: 8,
        fontSize: 14,
        color: '#4B5563'
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: '800',
        color: '#2C3E50'
    },
    sectionSubtitle: {
        fontSize: 14,
        color: '#4B5563'
    },
    habitCard: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 20,
        marginBottom: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.08,
        shadowRadius: 8,
        elevation: 4
    },
    habitHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 12
    },
    habitIndex: {
        fontSize: 18,
        fontWeight: '700',
        color: '#374151'
    },
    habitActions: {
        flexDirection: 'row',
        gap: 8
    },
    habitName: {
        fontSize: 18,
        color: '#1F2937',
        marginBottom: 16
    },
    editContainer: {
        marginBottom: 16
    },
    editButtons: {
        flexDirection: 'row',
        gap: 10,
        marginTop: 12
    },
    actionButton: {
        borderRadius: 14,
        paddingVertical: 10,
        paddingHorizontal: 16,
        alignItems: 'center',
        justifyContent: 'center'
    },
    actionButtonText: {
        color: '#FFFFFF',
        fontWeight: '700',
        fontSize: 16
    },
    editButton: {
        backgroundColor: '#2563EB'
    },
    deleteButton: {
        backgroundColor: '#DC2626'
    },
    saveButton: {
        backgroundColor: '#047857'
    },
    cancelButton: {
        backgroundColor: '#9CA3AF'
    },
    completeButton: {
        marginTop: 8,
        backgroundColor: '#F97316',
        borderRadius: 16,
        paddingVertical: 14,
        alignItems: 'center',
        justifyContent: 'center'
    },
    completeButtonText: {
        color: '#FFFFFF',
        fontWeight: '900',
        fontSize: 18
    },
    input: {
        backgroundColor: '#F3F4F6',
        borderRadius: 12,
        paddingHorizontal: 14,
        paddingVertical: 12,
        fontSize: 16,
        color: '#111827'
    },
    newHabitCard: {
        backgroundColor: '#FFFFFF',
        borderRadius: 20,
        padding: 20,
        marginBottom: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.08,
        shadowRadius: 8,
        elevation: 4,
        gap: 12
    },
    addButton: {
        backgroundColor: '#10B981'
    },
    errorContainer: {
        marginTop: 10,
        backgroundColor: '#FEE2E2',
        borderRadius: 12,
        padding: 12
    },
    errorText: {
        color: '#B91C1C',
        fontWeight: '700',
        textAlign: 'center'
    },
    emptyState: {
        backgroundColor: '#E0F2FE',
        borderRadius: 16,
        padding: 20,
        marginBottom: 20
    },
    emptyStateText: {
        fontSize: 18,
        fontWeight: '700',
        color: '#1D4ED8',
        marginBottom: 6
    },
    emptyStateDescription: {
        fontSize: 14,
        color: '#1E3A8A'
    }
})
