import React, { useRef } from 'react'
import { Text, View, StyleSheet, Animated, TouchableWithoutFeedback, Image } from 'react-native'
import { useLocalSearchParams } from 'expo-router'
import SSRImage from '../../../assets/SSR.png'
import SRImage from '../../../assets/SR.png'
import RImage from '../../../assets/R.png'
import NRImage from '../../../assets/NR.png'
import NImage from '../../../assets/N.png'
import DummyImage from '../../../assets/dummy.png'

const Result = (): JSX.Element => {
    const { name, rarity } = useLocalSearchParams<{name: string, rarity: string}>()
    const shakeAnimation = useRef(new Animated.Value(0)).current
    const imageOpacity = useRef(new Animated.Value(1)).current
    const textOpacity = useRef(new Animated.Value(0)).current

    const startShake = () => {
        // 1回分の震えアニメーションを定義
        const shakeSequence = [
            // 指定した時間をかけてtoValueまで変化
            Animated.timing(shakeAnimation, {
                toValue: 10,
                duration: 100,
                useNativeDriver: true
            }),
            Animated.timing(shakeAnimation, {
                toValue: -10,
                duration: 100,
                useNativeDriver: true
            }),
            Animated.timing(shakeAnimation, {
                toValue: 10,
                duration: 100,
                useNativeDriver: true
            }),
            Animated.timing(shakeAnimation, {
                toValue: 0,
                duration: 100,
                useNativeDriver: true
            })
        ]

        // 2回分のアニメーションを実行
        // 配列ないのアニメーションを順に実行
        Animated.sequence([
            ...shakeSequence,  // 1回目
            ...shakeSequence,  // 2回目
            // 画像をフェードアウト
            Animated.timing(imageOpacity, {
                toValue: 0,
                duration: 500,
                useNativeDriver: true
            }),
            // テキストをフェードイン
            Animated.timing(textOpacity, {
                toValue: 1,
                duration: 500,
                useNativeDriver: true
            })
        ]).start()
    }
    
    const getRarityColor = (rarity: string) => {
        switch (rarity) {
            case 'SSR':
                return 'linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3)'
            case 'SR':
                return '#FFD700'
            case 'R':
                return '#C0C0C0'
            case 'NR':
                return '#FF0000'
            default:
                return '#00FF00'
        }
    }

    const getRarityImage = (rarity: string) => {
        switch (rarity) {
            case 'SSR':
                return SSRImage
            case 'SR':
                return SRImage
            case 'R':
                return RImage
            case 'NR':
                return NRImage
            default:
                return NImage
        }
    }
    
    return (
        <TouchableWithoutFeedback onPress={startShake}>
            <View style={styles.container}>
                <Animated.Image 
                    source={getRarityImage(decodeURIComponent(rarity))}
                    style={[
                        styles.rarityImage,
                        {
                            transform: [{
                                translateX: shakeAnimation
                            }],
                            opacity: imageOpacity
                        }
                    ]}
                    resizeMode="contain"
                />
                <Animated.View style={[styles.textContainer, { opacity: textOpacity }]}>
                    <Text style={[
                        styles.rarityText,
                        { color: getRarityColor(decodeURIComponent(rarity)) }
                    ]}>
                        {decodeURIComponent(rarity)}
                    </Text>
                    <Text style={styles.name}>{decodeURIComponent(name)}</Text>
                    <Image 
                        source={DummyImage}
                        style={styles.dummyImage}
                        resizeMode="contain"
                    />
                </Animated.View>
            </View>
        </TouchableWithoutFeedback>
    )
}

export default Result 

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F8F0E3',
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    title: {
        fontSize: 28,
        fontWeight: '900',
        marginBottom: 20,
        color: '#2C3E50',
        textShadowColor: 'rgba(0, 0, 0, 0.1)',
        textShadowOffset: { width: 2, height: 2 },
        textShadowRadius: 3,
    },
    name: {
        fontSize: 36,
        fontWeight: '900',
        marginBottom: 20,
        color: '#2C3E50',
        textShadowColor: 'rgba(0, 0, 0, 0.1)',
        textShadowOffset: { width: 2, height: 2 },
        textShadowRadius: 3,
    },
    rarityImage: {
        width: 320,
        height: 320,
        marginBottom: 20,
    },
    rarityBox: {
        marginBottom: 20,
        padding: 15,
        borderRadius: 20,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 5,
    },
    rarityText: {
        fontSize: 52,
        fontWeight: '900',
        letterSpacing: 4,
        textShadowColor: 'rgba(0, 0, 0, 0.3)',
        textShadowOffset: { width: 3, height: 3 },
        textShadowRadius: 5,
    },
    textContainer: {
        position: 'absolute',
        alignItems: 'center',
        padding: 20,
        borderRadius: 30,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 4,
        },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 5,
    },
    dummyImage: {
        width: 240,
        height: 240,
        borderRadius: 20,
        marginTop: 20,
    }
});