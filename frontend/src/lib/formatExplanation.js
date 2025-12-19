/**
 * Format AI explanation text for better readability
 * Converts markdown-style formatting to React components
 */
export function formatExplanation(text) {
  if (!text) return null;

  // Split by common section markers
  const sections = [];
  const lines = text.split('\n');
  
  let currentSection = { title: '', content: [] };
  
  lines.forEach(line => {
    const trimmed = line.trim();
    
    // Skip empty lines
    if (!trimmed) {
      if (currentSection.content.length > 0) {
        currentSection.content.push({ type: 'break' });
      }
      return;
    }
    
    // Detect section headers (lines starting with *   ** or bullet points)
    if (trimmed.startsWith('*   **') || trimmed.startsWith('**')) {
      // Save previous section
      if (currentSection.title || currentSection.content.length > 0) {
        sections.push({ ...currentSection });
      }
      
      // Extract title between ** markers
      const titleMatch = trimmed.match(/\*\*([^*]+)\*\*/);
      if (titleMatch) {
        currentSection = { title: titleMatch[1].trim(), content: [] };
      }
    } 
    // Regular content line
    else {
      // Clean up markdown formatting
      let cleanLine = trimmed
        .replace(/^\*\s*/, '') // Remove leading asterisk
        .replace(/\*\*/g, '') // Remove bold markers
        .trim();
      
      if (cleanLine) {
        currentSection.content.push({ type: 'text', text: cleanLine });
      }
    }
  });
  
  // Add last section
  if (currentSection.title || currentSection.content.length > 0) {
    sections.push(currentSection);
  }
  
  return sections.filter(s => s.title || s.content.length > 0);
}

/**
 * Get color coding for health category
 */
export function getHealthColor(category) {
  const categoryLower = (category || '').toLowerCase();
  
  if (categoryLower.includes('healthy') || categoryLower.includes('good')) {
    return {
      gradient: 'from-green-500 to-emerald-500',
      bg: 'bg-green-500/10',
      border: 'border-green-500/30',
      text: 'text-green-300',
      icon: '✅'
    };
  }
  
  if (categoryLower.includes('moderate') || categoryLower.includes('average')) {
    return {
      gradient: 'from-yellow-500 to-orange-500',
      bg: 'bg-yellow-500/10',
      border: 'border-yellow-500/30',
      text: 'text-yellow-300',
      icon: '⚠️'
    };
  }
  
  // Harmful, Unhealthy, etc.
  return {
    gradient: 'from-red-500 to-rose-500',
    bg: 'bg-red-500/10',
    border: 'border-red-500/30',
    text: 'text-red-300',
    icon: '🚫'
  };
}
