house_patterns = [
    # Pattern 1: Classic Four-on-the-Floor
    {
        'pattern_num': 1,
        'genre': 'house',
        'tags': ['classic', 'four-on-the-floor'],
        'desc': 'Standard house beat with clap and hi-hats',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [0] * 16
    },
    # Pattern 2: Tech House with Offbeat Kick
    {
        'pattern_num': 2,
        'genre': 'house',
        'tags': ['tech', 'offbeat'],
        'desc': 'Tech house with extra kick on offbeat',
        'kick': [100, 0, 0, 0, 100, 0, 0, 90, 0, 0, 0, 100, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0] * 16,
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [0] * 16
    },
    # Pattern 3: Deep House with Ride
    {
        'pattern_num': 3,
        'genre': 'house',
        'tags': ['deep', 'ride'],
        'desc': 'Deep house with ride cymbal groove',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 50],
        'ch': [0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60],
        'ride': [80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0]
    },
    # Pattern 4: Minimal House
    {
        'pattern_num': 4,
        'genre': 'house',
        'tags': ['minimal'],
        'desc': 'Minimal house with sparse elements',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0] * 16,
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 5: Funky House
    {
        'pattern_num': 5,
        'genre': 'house',
        'tags': ['funky', 'syncopated'],
        'desc': 'Funky house with offbeat claps and ghost snares',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 100, 0, 0, 90, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [0] * 16
    },
    # Pattern 6: Tribal House
    {
        'pattern_num': 6,
        'genre': 'house',
        'tags': ['tribal', 'percussive'],
        'desc': 'Tribal house with heavy tom usage',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0] * 16,
        'tom': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 7: Acid House
    {
        'pattern_num': 7,
        'genre': 'house',
        'tags': ['acid', 'syncopated'],
        'desc': 'Acid house with syncopated kicks and toms',
        'kick': [100, 0, 0, 0, 100, 0, 0, 90, 0, 0, 0, 100, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 80, 0, 80],
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 60, 0, 0, 0, 60, 0, 0, 0, 60, 0, 0, 0, 60],
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [0] * 16
    },
    # Pattern 8: Progressive House
    {
        'pattern_num': 8,
        'genre': 'house',
        'tags': ['progressive', 'build-up'],
        'desc': 'Progressive house with building hi-hats and ride',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 80, 80],
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0]
    },
    # Pattern 9: Disco House
    {
        'pattern_num': 9,
        'genre': 'house',
        'tags': ['disco', 'funky'],
        'desc': 'Disco house with ride and open hi-hats',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0]
    },
    # Pattern 10: Afro House
    {
        'pattern_num': 10,
        'genre': 'house',
        'tags': ['afro', 'percussive'],
        'desc': 'Afro house with tribal tom patterns',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0] * 16,
        'tom': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 11: Jackin’ House with Swing
    {
        'pattern_num': 11,
        'genre': 'house',
        'tags': ['jackin', 'swing'],
        'desc': 'Jackin’ house with swung hi-hats and offbeat kicks',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 100, 0, 0, 90, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 70, 0, 80, 0, 0, 0, 80, 0, 70, 0, 80, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 12: Chicago House with Double Snares
    {
        'pattern_num': 12,
        'genre': 'house',
        'tags': ['chicago', 'double-snares'],
        'desc': 'Chicago house with double snares for extra groove',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 90],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [0] * 16
    },
    # Pattern 13: Melodic House with Atmospheric Hi-hats
    {
        'pattern_num': 13,
        'genre': 'house',
        'tags': ['melodic', 'atmospheric'],
        'desc': 'Melodic house with soft, spacious hi-hats',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0],
        'oh': [0, 0, 0, 50, 0, 0, 0, 50, 0, 0, 0, 50, 0, 0, 0, 50],
        'ch': [0, 60, 0, 0, 0, 60, 0, 0, 0, 60, 0, 0, 0, 60, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 14: Latin House with Polyrhythms
    {
        'pattern_num': 14,
        'genre': 'house',
        'tags': ['latin', 'polyrhythmic'],
        'desc': 'Latin house with polyrhythmic toms and claps',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 80, 0, 70, 0, 80, 0, 0, 0, 80, 0, 70, 0, 80, 0, 0],
        'clap': [0, 0, 0, 90, 0, 0, 0, 80, 0, 0, 0, 90, 0, 0, 0, 80],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 15: Garage House Hybrid
    {
        'pattern_num': 15,
        'genre': 'house',
        'tags': ['garage-house', 'swing'],
        'desc': 'House with UKG-inspired swung kicks and snares',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 100, 0, 0, 90, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 70, 0, 80, 0, 0, 0, 80, 0, 70, 0, 80, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 16: Lo-Fi House with Crunchy Snares
    {
        'pattern_num': 16,
        'genre': 'house',
        'tags': ['lo-fi', 'crunchy'],
        'desc': 'Lo-fi house with crunchy snares and muted kicks',
        'kick': [80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 70, 0, 0, 0, 0, 0, 0, 0, 70, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 50],
        'ch': [0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60],
        'ride': [0] * 16
    },
    # Pattern 17: Big Room House with Build-Up
    {
        'pattern_num': 17,
        'genre': 'house',
        'tags': ['big-room', 'build-up'],
        'desc': 'Big room house with snare rolls for tension',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 80, 80, 80],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 18: French House with Filter Sweep
    {
        'pattern_num': 18,
        'genre': 'house',
        'tags': ['french', 'funky'],
        'desc': 'French house with funky claps and hi-hats',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'ride': [0] * 16
    },
    # Pattern 19: Tropical House with Offbeat Percussion
    {
        'pattern_num': 19,
        'genre': 'house',
        'tags': ['tropical', 'offbeat'],
        'desc': 'Tropical house with offbeat toms and claps',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80],
        'clap': [0, 0, 0, 90, 0, 0, 0, 90, 0, 0, 0, 90, 0, 0, 0, 90],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 20: Future House with Bass-Driven Kick
    {
        'pattern_num': 20,
        'genre': 'house',
        'tags': ['future', 'bass-driven'],
        'desc': 'Future house with punchy kicks and minimal hi-hats',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 100, 0, 0, 90, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    }
]

ukg_patterns = [
    # Pattern 1: Classic 2-Step
    {
        'pattern_num': 21,
        'genre': 'ukg',
        'tags': ['2-step', 'classic'],
        'desc': 'Classic UKG 2-step with swung hi-hats',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 2: Speed Garage
    {
        'pattern_num': 22,
        'genre': 'ukg',
        'tags': ['speed-garage', 'double-kicks'],
        'desc': 'Speed garage with double kicks',
        'kick': [100, 0, 90, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 90, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 3: Soulful UKG
    {
        'pattern_num': 23,
        'genre': 'ukg',
        'tags': ['soulful', 'smooth'],
        'desc': 'Soulful UKG with soft snares and open hi-hats',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 0, 0, 70, 0, 70, 0, 70, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 4: Bassline UKG
    {
        'pattern_num': 24,
        'genre': 'ukg',
        'tags': ['bassline', 'aggressive'],
        'desc': 'Bassline UKG with double kicks and syncopated snares',
        'kick': [100, 0, 90, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 90, 0],
        'snare': [0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 5: Grime-Influenced UKG
    {
        'pattern_num': 25,
        'genre': 'ukg',
        'tags': ['grime', 'broken'],
        'desc': 'Grime-influenced UKG with broken kick and snare',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 80, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 6: Dark UKG
    {
        'pattern_num': 26,
        'genre': 'ukg',
        'tags': ['dark', 'minimal'],
        'desc': 'Dark UKG with sparse kicks and eerie hi-hats',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0] * 16,
        'tom': [0] * 16,
        'clap': [0, 0, 0, 0, 90, 0, 0, 0, 0, 0, 0, 0, 90, 0, 0, 0],
        'oh': [0] * 16,
        'ch': [0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60, 0, 60],
        'ride': [0] * 16
    },
    # Pattern 7: UKG with Swing
    {
        'pattern_num': 27,
        'genre': 'ukg',
        'tags': ['swing', '2-step'],
        'desc': 'UKG with heavy swing on hi-hats and snares',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 0, 0, 70, 0, 70, 0, 70, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 8: UKG with Percussion
    {
        'pattern_num': 28,
        'genre': 'ukg',
        'tags': ['percussive', '2-step'],
        'desc': 'UKG with additional tom percussion',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 9: UKG with Breakbeat Influence
    {
        'pattern_num': 29,
        'genre': 'ukg',
        'tags': ['breakbeat', 'choppy'],
        'desc': 'UKG with choppy breakbeat-inspired patterns',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 80, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 10: UKG with Vocal Chops
    {
        'pattern_num': 30,
        'genre': 'ukg',
        'tags': ['vocal-chops', '2-step'],
        'desc': 'UKG with space for vocal chops',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 0, 0, 70, 0, 70, 0, 70, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 11: 4x4 UKG with Heavy Swing
    {
        'pattern_num': 31,
        'genre': 'ukg',
        'tags': ['4x4', 'swing'],
        'desc': '4x4 UKG with swung hi-hats and offbeat claps',
        'kick': [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80],
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 0, 0, 70, 0, 70, 0, 70, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 12: UKG with Snare Rolls
    {
        'pattern_num': 32,
        'genre': 'ukg',
        'tags': ['snare-rolls', '2-step'],
        'desc': '2-step UKG with snare rolls for tension',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 80, 80, 80],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 13: Dub UKG with Space
    {
        'pattern_num': 33,
        'genre': 'ukg',
        'tags': ['dub', 'spacey'],
        'desc': 'Dub-influenced UKG with sparse kicks and echoey snares',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 0, 0, 70, 0, 70, 0, 70, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 14: UKG with Offbeat Claps
    {
        'pattern_num': 34,
        'genre': 'ukg',
        'tags': ['offbeat-claps', '2-step'],
        'desc': '2-step UKG with offbeat claps for groove',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80],
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 15: Minimal UKG with Tom Accents
    {
        'pattern_num': 35,
        'genre': 'ukg',
        'tags': ['minimal', 'tom-accents'],
        'desc': 'Minimal UKG with subtle tom accents',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 16: UKG with Jungle Influence
    {
        'pattern_num': 36,
        'genre': 'ukg',
        'tags': ['jungle', 'choppy'],
        'desc': 'UKG with jungle-inspired choppy kicks',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 80, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 17: UKG with Polyrhythmic Toms
    {
        'pattern_num': 37,
        'genre': 'ukg',
        'tags': ['polyrhythmic', 'percussive'],
        'desc': 'UKG with polyrhythmic tom layers',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 80, 0, 70, 0, 80, 0, 0, 0, 80, 0, 70, 0, 80, 0, 0],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 18: UKG with Fast Hi-hats
    {
        'pattern_num': 38,
        'genre': 'ukg',
        'tags': ['fast-hats', '2-step'],
        'desc': '2-step UKG with rapid hi-hat patterns',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 19: UKG with Garage Shuffle
    {
        'pattern_num': 39,
        'genre': 'ukg',
        'tags': ['shuffle', '2-step'],
        'desc': 'UKG with shuffled kicks and snares',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 90],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 20: UKG with Dubstep Influence
    {
        'pattern_num': 40,
        'genre': 'ukg',
        'tags': ['dubstep', 'dark'],
        'desc': 'UKG with dubstep-inspired half-time feel',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    }
]

dnb_patterns = [
    # Pattern 1: Basic Breakbeat
    {
        'pattern_num': 41,
        'genre': 'dnb',
        'tags': ['breakbeat', 'classic'],
        'desc': 'Basic DnB breakbeat pattern',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 2: Jungle Break
    {
        'pattern_num': 42,
        'genre': 'dnb',
        'tags': ['jungle', 'choppy'],
        'desc': 'Jungle-inspired choppy breakbeat',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 80, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 3: Liquid DnB
    {
        'pattern_num': 43,
        'genre': 'dnb',
        'tags': ['liquid', 'smooth'],
        'desc': 'Smooth liquid DnB with soft snares',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 4: Neurofunk
    {
        'pattern_num': 44,
        'genre': 'dnb',
        'tags': ['neurofunk', 'intricate'],
        'desc': 'Neurofunk with intricate snare patterns',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 5: Jump-Up
    {
        'pattern_num': 45,
        'genre': 'dnb',
        'tags': ['jump-up', 'bouncy'],
        'desc': 'Jump-up DnB with bouncy kick and snare',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 6: Amen Break Variation
    {
        'pattern_num': 46,
        'genre': 'dnb',
        'tags': ['amen', 'jungle'],
        'desc': 'Variation of the Amen break with ghost snares',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 7: Half-Time DnB
    {
        'pattern_num': 47,
        'genre': 'dnb',
        'tags': ['half-time', 'heavy'],
        'desc': 'Half-time DnB with heavy kicks and snares',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 8: Techstep
    {
        'pattern_num': 48,
        'genre': 'dnb',
        'tags': ['techstep', 'dark'],
        'desc': 'Techstep DnB with dark, punchy kicks',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 9: Jazz-Influenced DnB
    {
        'pattern_num': 49,
        'genre': 'dnb',
        'tags': ['jazz', 'swing'],
        'desc': 'Jazz-influenced DnB with swung ride',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0, 80, 0, 70, 0, 80, 0, 0, 0, 80, 0, 70, 0, 80, 0, 0]
    },
    # Pattern 10: Minimal DnB
    {
        'pattern_num': 50,
        'genre': 'dnb',
        'tags': ['minimal', 'sparse'],
        'desc': 'Minimal DnB with sparse kicks and snares',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 11: Drumfunk with Choppy Snares
    {
        'pattern_num': 51,
        'genre': 'dnb',
        'tags': ['drumfunk', 'choppy'],
        'desc': 'Drumfunk with intricate, choppy snares',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 80, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 12: Atmospheric DnB
    {
        'pattern_num': 52,
        'genre': 'dnb',
        'tags': ['atmospheric', 'spacey'],
        'desc': 'Atmospheric DnB with space for pads',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 60],
        'ch': [0, 70, 0, 70, 0, 70, 0, 0, 0, 70, 0, 70, 0, 70, 0, 0],
        'ride': [0] * 16
    },
    # Pattern 13: Ragga Jungle
    {
        'pattern_num': 53,
        'genre': 'dnb',
        'tags': ['ragga', 'jungle'],
        'desc': 'Ragga jungle with aggressive kicks and toms',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 80, 0, 0, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 14: Neurofunk with Double Kicks
    {
        'pattern_num': 54,
        'genre': 'dnb',
        'tags': ['neurofunk', 'double-kicks'],
        'desc': 'Neurofunk with double kicks and ghost snares',
        'kick': [100, 0, 90, 0, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 90, 0],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 15: Jump-Up with Snare Fills
    {
        'pattern_num': 55,
        'genre': 'dnb',
        'tags': ['jump-up', 'snare-fills'],
        'desc': 'Jump-up DnB with snare fills for energy',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 80, 80, 80],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    },
    # Pattern 16: Liquid Funk with Ride
    {
        'pattern_num': 56,
        'genre': 'dnb',
        'tags': ['liquid-funk', 'ride'],
        'desc': 'Liquid funk with smooth ride cymbals',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80]
    },
    # Pattern 17: DnB with Polyrhythmic Snares
    {
        'pattern_num': 57,
        'genre': 'dnb',
        'tags': ['polyrhythmic', 'complex'],
        'desc': 'DnB with polyrhythmic snare patterns',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 80, 0, 0, 0, 0, 90, 0, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 18: DnB with Breakcore Influence
    {
        'pattern_num': 58,
        'genre': 'dnb',
        'tags': ['breakcore', 'chaotic'],
        'desc': 'Breakcore-inspired DnB with chaotic breaks',
        'kick': [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 90],
        'snare': [0, 0, 0, 0, 100, 0, 40, 0, 0, 0, 0, 0, 100, 0, 40, 0],
        'tom': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 80, 0, 80],
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 19: DnB with Fast Hi-hats
    {
        'pattern_num': 59,
        'genre': 'dnb',
        'tags': ['fast-hats', 'energetic'],
        'desc': 'DnB with rapid hi-hat patterns',
        'kick': [100, 0, 0, 90, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70, 0, 70, 60, 70],
        'ride': [0] * 16
    },
    # Pattern 20: DnB with Dubstep Half-Time
    {
        'pattern_num': 60,
        'genre': 'dnb',
        'tags': ['dubstep', 'half-time'],
        'desc': 'DnB with dubstep-inspired half-time groove',
        'kick': [100, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'snare': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0],
        'tom': [0] * 16,
        'clap': [0] * 16,
        'oh': [0] * 16,
        'ch': [0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70],
        'ride': [0] * 16
    }
]

all_patterns = house_patterns + ukg_patterns + dnb_patterns