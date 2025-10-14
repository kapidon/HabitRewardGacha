import React from 'react'
import { Stack } from 'expo-router'
import { SQLiteProvider, type SQLiteDatabase } from 'expo-sqlite'

const initializeDatabase = async (db: SQLiteDatabase): Promise<void> => {
    await db.execAsync(`
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    `)
    await db.execAsync(`
        CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total INTEGER NOT NULL
        );
    `)
    await db.runAsync('INSERT OR IGNORE INTO points (id, total) VALUES (1, 0)')
}

const Layout = (): JSX.Element => {
    return (
        <SQLiteProvider
            databaseName="habit_rewards.db"
            onInit={initializeDatabase}
            onError={(error) => {
                console.error('SQLiteProvider error', error)
            }}
        >
            <Stack
                screenOptions={{
                    headerStyle: {
                        backgroundColor: '#467FD3',
                    },
                    headerTintColor: '#ffffff',
                    headerTitle: 'RewardGacha',
                    headerBackTitle: 'Back',
                    headerTitleStyle: {
                        fontSize: 22,
                        fontWeight: 'bold',
                    }
                }}
            >
                <Stack.Screen name="index" options={{ title: 'ホーム' }} />
                <Stack.Screen name="gacha/pull" options={{ title: 'ガチャを引く' }} />
                <Stack.Screen name="gacha/result" options={{ title: 'ガチャ結果' }} />
            </Stack>
        </SQLiteProvider>
    )
}

export default Layout
