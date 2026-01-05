import React from 'react'

const Logo = ({ size = 28, className = '' }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ minWidth: size }}
    >
      {/* Outer ring - Nano tech feel */}
      <circle cx="16" cy="16" r="14" stroke="currentColor" strokeWidth="1.5" strokeOpacity="0.15" />
      
      {/* The "BigOne" B shape abstract - Top part */}
      <path 
        d="M9 7H15C19 7 21 9 21 12.5C21 15.5 19 16.5 16 16.5H9V7Z" 
        stroke="currentColor" 
        strokeWidth="2.5" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      />
      
      {/* The "Banana" Swoosh - forming the bottom of the B / Dynamic curve */}
      <path 
        d="M9 16.5V25H13C18 25 22.5 22 23.5 16.5" 
        stroke="var(--accent-yellow, #d29922)" 
        strokeWidth="2.5" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      />
      
      {/* Central dot/target accent */}
      <circle cx="13.5" cy="16.5" r="2" fill="var(--accent-yellow, #d29922)" />
    </svg>
  )
}

export default Logo
