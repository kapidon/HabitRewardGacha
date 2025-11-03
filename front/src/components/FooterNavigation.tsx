import React, { useMemo } from 'react'
import { View, TouchableOpacity, StyleSheet } from 'react-native'
import { MaterialCommunityIcons } from '@expo/vector-icons'
import { useRouter, useSegments } from 'expo-router'
import { useSafeAreaInsets } from 'react-native-safe-area-context'

type NavigationItem = {
    key: string
    icon: keyof typeof MaterialCommunityIcons.glyphMap
    href: string
    matchPaths?: string[]
}

// 画面下部に配置するナビゲーションボタンの一覧
const navigationItems: NavigationItem[] = [
    {
        key: 'home',
        icon: 'home',
        href: '/',
        matchPaths: ['/']
    },
    {
        key: 'gacha',
        icon: 'slot-machine',
        href: '/gacha/pull',
        matchPaths: ['/gacha']
    }
]

type FooterNavigationProps = {
    reservedHeight: number
}

const FooterNavigation = ({ reservedHeight }: FooterNavigationProps): JSX.Element => {
    const router = useRouter()
    const segments = useSegments()
    const insets = useSafeAreaInsets()

    const currentPath = `/${segments.join('/')}`.replace('//', '/') || '/'

    const containerStyle = useMemo(() => ([
        styles.container,
        {
            paddingBottom: Math.max(insets.bottom, 12),
            height: reservedHeight + Math.max(insets.bottom, 12)
        }
    ]), [insets.bottom, reservedHeight])

    const handlePress = (href: string) => {
        if (currentPath === href) {
            return
        }

        router.push(href)
    }

    return (
        <View style={containerStyle}>
            {navigationItems.map((item) => {
                const isActive = item.matchPaths?.some((path) => currentPath.startsWith(path)) ?? false

                return (
                    <TouchableOpacity
                        key={item.key}
                        onPress={() => handlePress(item.href)}
                        style={styles.button}
                        activeOpacity={0.7}
                    >
                        <MaterialCommunityIcons
                            name={item.icon}
                            size={28}
                            color={isActive ? '#FFFFFF' : 'rgba(255, 255, 255, 0.7)'}
                        />
                    </TouchableOpacity>
                )
            })}
        </View>
    )
}

export default FooterNavigation

const styles = StyleSheet.create({
    container: {
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        backgroundColor: '#ADD8E6',
        borderTopLeftRadius: 16,
        borderTopRightRadius: 16,
        shadowColor: '#000000',
        shadowOffset: { width: 0, height: -2 },
        shadowOpacity: 0.12,
        shadowRadius: 6,
        elevation: 6,
        paddingHorizontal: 24
    },
    button: {
        padding: 12
    }
})
