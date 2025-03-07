// Medi Mind Logo Path (medical cross with brain elements)
const MEDI_MIND_LOGO_PATH = "M50 0C77.6 0 100 22.4 100 50C100 77.6 77.6 100 50 100C22.4 100 0 77.6 0 50C0 22.4 22.4 0 50 0ZM50 10C27.9 10 10 27.9 10 50C10 72.1 27.9 90 50 90C72.1 90 90 72.1 90 50C90 27.9 72.1 10 50 10ZM40 25H60V75H40V25ZM25 40H75V60H25V40ZM30 65C35 75 45 80 50 80C55 80 65 75 70 65C65 70 55 72 50 72C45 72 35 70 30 65ZM30 35C35 25 45 20 50 20C55 20 65 25 70 35C65 30 55 28 50 28C45 28 35 30 30 35Z";

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('particleCanvas');
  const ctx = canvas.getContext('2d');
  
  let mousePosition = { x: 0, y: 0 };
  let isTouching = false;
  let isMobile = false;
  let particles = [];
  let textImageData = null;
  let animationFrameId;

  // Add stars to the background
  const stars = [];
  const starCount = 200;

  function createStars() {
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 1,
        opacity: Math.random(),
        speed: Math.random() * 0.5 + 0.1,
      });
    }
  }

  function drawStars() {
    ctx.fillStyle = 'white';
    for (let i = 0; i < stars.length; i++) {
      const star = stars[i];
      ctx.globalAlpha = star.opacity;
      ctx.fillRect(star.x, star.y, star.size, star.size);
      star.y += star.speed; // Move stars downward
      if (star.y > canvas.height) {
        star.y = 0; // Reset star to the top
        star.x = Math.random() * canvas.width;
      }
    }
    ctx.globalAlpha = 1; // Reset opacity
  }

  // Call createStars() in the initialization
  createStars();
  
  // Update canvas size
  function updateCanvasSize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    isMobile = window.innerWidth < 768;
  }
  
  updateCanvasSize();
  
  // Create text image
  function createTextImage() {
    if (!ctx || !canvas) return 0;
    
    ctx.fillStyle = 'white';
    ctx.save();
    
    const logoHeight = isMobile ? 150 : 200;
    const logoWidth = logoHeight;
    
    // Calculate the position for the logo and text (move to the left)
    const totalWidth = logoWidth + 200; // Logo width + text width (adjust as needed)
    const startX = (canvas.width - totalWidth) / 2 - 230; // Center the logo and text
    const startY = (canvas.height - logoHeight) / 2; // Center vertically
    
    // Draw Medi Mind logo
    const logoScale = logoHeight / 110;
    ctx.translate(startX, startY);
    ctx.scale(logoScale, logoScale);
    const path = new Path2D(MEDI_MIND_LOGO_PATH);
    ctx.fill(path);
    
    // Draw "MediMind" text beside the logo
    ctx.font = `${logoHeight * 0.4}px Arial`; // Reduced font size
    ctx.fillText("MediMind", 120, 78); // Adjusted position
    
    ctx.restore();
    
    textImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    return logoScale;
  }
  
  // Create a particle
  function createParticle(scale) {
    if (!ctx || !canvas || !textImageData) return null;
    
    const data = textImageData.data;
    
    for (let attempt = 0; attempt < 100; attempt++) {
      const x = Math.floor(Math.random() * canvas.width);
      const y = Math.floor(Math.random() * canvas.height);
      
      if (data[(y * canvas.width + x) * 4 + 3] > 128) {
        return {
          x: x,
          y: y,
          baseX: x,
          baseY: y,
          size: Math.random() * 1 + 0.5,
          color: 'white',
          scatteredColor: Math.random() > 0.5 ? '#4cc9f0' : '#0077b6', // Medical blue colors
          life: Math.random() * 100 + 50
        };
      }
    }
    
    return null;
  }
  
  // Create initial particles
  function createInitialParticles(scale) {
    const baseParticleCount = 7000;
    const particleCount = Math.floor(baseParticleCount * Math.sqrt((canvas.width * canvas.height) / (1920 * 1080)));
    for (let i = 0; i < particleCount; i++) {
      const particle = createParticle(scale);
      if (particle) particles.push(particle);
    }
  }
  
  // Animation function
  function animate(scale) {
    if (!ctx || !canvas) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw stars
    drawStars();
    
    const { x: mouseX, y: mouseY } = mousePosition;
    const maxDistance = 240;
    
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      const dx = mouseX - p.x;
      const dy = mouseY - p.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < maxDistance && (isTouching || !('ontouchstart' in window))) {
        const force = (maxDistance - distance) / maxDistance;
        const angle = Math.atan2(dy, dx);
        const moveX = Math.cos(angle) * force * 60;
        const moveY = Math.sin(angle) * force * 60;
        p.x = p.baseX - moveX;
        p.y = p.baseY - moveY;
        
        ctx.fillStyle = p.scatteredColor;
      } else {
        p.x += (p.baseX - p.x) * 0.1;
        p.y += (p.baseY - p.y) * 0.1;
        ctx.fillStyle = 'white';
      }
      
      ctx.fillRect(p.x, p.y, p.size, p.size);
      
      p.life--;
      if (p.life <= 0) {
        const newParticle = createParticle(scale);
        if (newParticle) {
          particles[i] = newParticle;
        } else {
          particles.splice(i, 1);
          i--;
        }
      }
    }
    
    const baseParticleCount = 7000;
    const targetParticleCount = Math.floor(baseParticleCount * Math.sqrt((canvas.width * canvas.height) / (1920 * 1080)));
    while (particles.length < targetParticleCount) {
      const newParticle = createParticle(scale);
      if (newParticle) particles.push(newParticle);
    }
    
    animationFrameId = requestAnimationFrame(() => animate(scale));
  }
  
  // Event handlers
  function handleResize() {
    updateCanvasSize();
    const newScale = createTextImage();
    particles = [];
    createInitialParticles(newScale);
  }
  
  function handleMove(x, y) {
    mousePosition = { x, y };
  }
  
  function handleMouseMove(e) {
    handleMove(e.clientX, e.clientY);
  }
  
  function handleTouchMove(e) {
    if (e.touches.length > 0) {
      e.preventDefault();
      handleMove(e.touches[0].clientX, e.touches[0].clientY);
    }
  }
  
  function handleTouchStart() {
    isTouching = true;
  }
  
  function handleTouchEnd() {
    isTouching = false;
    mousePosition = { x: 0, y: 0 };
  }
  
  function handleMouseLeave() {
    if (!('ontouchstart' in window)) {
      mousePosition = { x: 0, y: 0 };
    }
  }
  
  // Add event listeners
  window.addEventListener('resize', handleResize);
  canvas.addEventListener('mousemove', handleMouseMove);
  canvas.addEventListener('touchmove', handleTouchMove, { passive: false });
  canvas.addEventListener('mouseleave', handleMouseLeave);
  canvas.addEventListener('touchstart', handleTouchStart);
  canvas.addEventListener('touchend', handleTouchEnd);
  
  // Initialize
  const scale = createTextImage();
  createInitialParticles(scale);
  animate(scale);
});