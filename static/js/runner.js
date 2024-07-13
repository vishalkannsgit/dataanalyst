window.onload = function() {
    const runner = document.querySelector('.runner');
    const runnerWidth = runner.scrollWidth;

    runner.style.animationDuration = `${runnerWidth / 50}s`; // Adjust duration based on content width
}
