import { Variants } from 'framer-motion';

// Durações padrão para animações
export const DURATION = {
  FAST: 0.2,
  NORMAL: 0.3,
  SLOW: 0.5,
  VERY_SLOW: 0.8,
};

// Curvas de easing padrão
export const EASING = {
  EASE_IN_OUT: [0.4, 0, 0.2, 1],
  EASE_OUT: [0, 0, 0.2, 1],
  EASE_IN: [0.4, 0, 1, 1],
  SHARP: [0.4, 0, 0.6, 1],
};

// Variantes de animação para elementos que aparecem/desaparecem
export const fadeVariants: Variants = {
  hidden: {
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que deslizam
export const slideVariants: Variants = {
  hidden: {
    x: -20,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    x: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com escala
export const scaleVariants: Variants = {
  hidden: {
    scale: 0.8,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que giram
export const rotateVariants: Variants = {
  hidden: {
    rotate: -180,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    rotate: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com bounce
export const bounceVariants: Variants = {
  hidden: {
    y: 20,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: [0.34, 1.56, 0.64, 1], // Curva de bounce
    },
  },
};

// Variantes para elementos que aparecem com stagger (sequência)
export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

// Variantes para elementos que aparecem com fade e slide
export const fadeSlideVariants: Variants = {
  hidden: {
    y: 20,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com fade e scale
export const fadeScaleVariants: Variants = {
  hidden: {
    scale: 0.9,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com fade e rotate
export const fadeRotateVariants: Variants = {
  hidden: {
    rotate: -10,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    rotate: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com fade e bounce
export const fadeBounceVariants: Variants = {
  hidden: {
    y: 20,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: [0.34, 1.56, 0.64, 1], // Curva de bounce
    },
  },
};

// Variantes para elementos que aparecem com fade e slide horizontal
export const fadeSlideHorizontalVariants: Variants = {
  hidden: {
    x: -20,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    x: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com fade e slide vertical
export const fadeSlideVerticalVariants: Variants = {
  hidden: {
    y: 20,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com fade e scale horizontal
export const fadeScaleHorizontalVariants: Variants = {
  hidden: {
    scaleX: 0,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    scaleX: 1,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
};

// Variantes para elementos que aparecem com fade e scale vertical
export const fadeScaleVerticalVariants: Variants = {
  hidden: {
    scaleY: 0,
    opacity: 0,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_OUT,
    },
  },
  visible: {
    scaleY: 1,
    opacity: 1,
    transition: {
      duration: DURATION.NORMAL,
      ease: EASING.EASE_IN,
    },
  },
}; 
