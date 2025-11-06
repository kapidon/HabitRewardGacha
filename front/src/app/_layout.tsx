import React, { useEffect } from 'react'
import { Stack } from 'expo-router'

import { initializeHabitTable } from '../database/habitTable'

const Layout = (): JSX.Element => {
    useEffect(() => {
        const setupDatabase = async (): Promise<void> => {
            try {
                await initializeHabitTable()
            } catch (error) {
                console.error('Failed to initialize habit table', error)
            }
        }

        void setupDatabase()
    }, [])

    return (
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
                },
            }}
        />
    )
}

export default Layout
