/**
 * Format AI explanation text for better readability
 * Converts markdown-style formatting to React components
 */
export function formatExplanation(text) {
  if (!text) return null;

  // Split into lines and parse markdown-like sections and bullets
  const sections = [];
  const lines = text.split('\n');
  let currentSection = { title: '', content: [] };

  const pushCurrentSection = () => {
    if (currentSection.title || currentSection.content.length > 0) {
      sections.push({ ...currentSection });
    }
  };

  const cleanInlineMarkdown = (value) => {
    return value
      .replace(/\*\*(.*?)\*\*/g, '$1')
      .replace(/`([^`]+)`/g, '$1')
      .trim();
  };

  lines.forEach(line => {
    const trimmed = line.trim();

    // Skip empty lines
    if (!trimmed) {
      if (currentSection.content.length > 0) {
        currentSection.content.push({ type: 'break' });
      }
      return;
    }

    // Detect markdown heading: ## Title
    if (trimmed.startsWith('## ')) {
      pushCurrentSection();
      currentSection = {
        title: cleanInlineMarkdown(trimmed.replace(/^##\s+/, '')),
        content: []
      };
      return;
    }

    // Detect bold heading: **Title**
    if (/^\*\*[^*]+\*\*$/.test(trimmed)) {
      pushCurrentSection();
      currentSection = {
        title: cleanInlineMarkdown(trimmed),
        content: []
      };
      return;
    }

    // Detect bullet item
    if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
      const bulletText = cleanInlineMarkdown(trimmed.replace(/^[-•]\s+/, ''));
      if (bulletText) {
        currentSection.content.push({ type: 'bullet', text: bulletText });
      }
      return;
    }

    const cleanLine = cleanInlineMarkdown(trimmed);
    if (cleanLine) {
      currentSection.content.push({ type: 'text', text: cleanLine });
    }
  });

  // Add last section
  pushCurrentSection();

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
