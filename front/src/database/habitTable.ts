import { openDatabase, type SQLiteDatabase } from 'expo-sqlite'

let databaseInstance: SQLiteDatabase | null = null

const getDatabase = (): SQLiteDatabase => {
    if (databaseInstance !== null) {
        return databaseInstance
    }

    databaseInstance = openDatabase('habits.db')
    return databaseInstance
}

export const initializeHabitTable = async (): Promise<void> => {
    const db = getDatabase()

    await new Promise<void>((resolve, reject) => {
        db.transaction(
            (transaction) => {
                transaction.executeSql(
                    `CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        is_achieved INTEGER NOT NULL DEFAULT 0,
                        last_achieved_at TEXT,
                        consecutive_days INTEGER NOT NULL DEFAULT 0
                    );`,
                    [],
                    () => resolve(),
                    (_transaction, error) => {
                        reject(error)
                        return false
                    },
                )
            },
            (error) => {
                reject(error)
            },
        )
    })
}
