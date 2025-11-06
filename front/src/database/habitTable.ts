import { openDatabaseAsync, type SQLiteDatabase } from 'expo-sqlite'

let databasePromise: Promise<SQLiteDatabase> | null = null

const getDatabase = async (): Promise<SQLiteDatabase> => {
    if (databasePromise == null) {
        databasePromise = openDatabaseAsync('habits.db')
    }

    return databasePromise
}

export const initializeHabitTable = async (): Promise<void> => {
    const db = await getDatabase()

    await db.execAsync('PRAGMA journal_mode = WAL;')

    await db.withTransactionAsync(async () => {
        await db.runAsync(`
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_achieved INTEGER NOT NULL DEFAULT 0,
                last_achieved_at TEXT,
                consecutive_days INTEGER NOT NULL DEFAULT 0
            )
        `)
    })
}

export const getHabitDatabase = async (): Promise<SQLiteDatabase> => getDatabase()
