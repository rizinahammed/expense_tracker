document.addEventListener('DOMContentLoaded', () => {
    const svg = document.getElementById('income-expense-chart');
    const tooltip = document.getElementById('chart-tooltip');
    const dataScript = document.getElementById('category-chart-data');

    if (!svg || !dataScript) {
        return;
    }

    let chartData;
    try {
        chartData = JSON.parse(dataScript.textContent || '[]');
    } catch (error) {
        chartData = [];
    }

    if (!Array.isArray(chartData) || chartData.length === 0) {
        return;
    }

    const svgNS = 'http://www.w3.org/2000/svg';
    const currency = (value) => `₹${Number(value || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;

    const createNode = (name, attrs = {}, className = '') => {
        const node = document.createElementNS(svgNS, name);
        Object.entries(attrs).forEach(([key, val]) => node.setAttribute(key, String(val)));
        if (className) {
            node.setAttribute('class', className);
        }
        return node;
    };

    const showTooltip = (event, categoryName, kind, value) => {
        if (!tooltip) return;
        tooltip.innerHTML = `<strong>${categoryName}</strong><br>${kind}: ${currency(value)}`;
        tooltip.classList.add('show');

        const rect = svg.getBoundingClientRect();
        const offsetX = event.clientX - rect.left;
        const offsetY = event.clientY - rect.top;
        tooltip.style.left = `${offsetX}px`;
        tooltip.style.top = `${offsetY}px`;
    };

    const hideTooltip = () => {
        if (!tooltip) return;
        tooltip.classList.remove('show');
    };

    const renderChart = () => {
        const width = svg.clientWidth || 900;
        const height = svg.clientHeight || 360;
        svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
        svg.innerHTML = '';

        const margin = { top: 22, right: 14, bottom: 76, left: 52 };
        const innerWidth = Math.max(220, width - margin.left - margin.right);
        const innerHeight = Math.max(140, height - margin.top - margin.bottom);

        const maxValue = Math.max(
            1,
            ...chartData.map((item) => Math.max(Number(item.income || 0), Number(item.expense || 0)))
        );

        const roundedMax = Math.ceil(maxValue / 1000) * 1000;
        const yTicks = 5;

        const chartGroup = createNode('g', { transform: `translate(${margin.left},${margin.top})` });
        svg.appendChild(chartGroup);

        for (let i = 0; i <= yTicks; i += 1) {
            const value = (roundedMax / yTicks) * i;
            const y = innerHeight - (value / roundedMax) * innerHeight;

            chartGroup.appendChild(
                createNode('line', { x1: 0, y1: y, x2: innerWidth, y2: y }, 'chart-grid-line')
            );

            const tickLabel = createNode('text', { x: -10, y: y + 4, 'text-anchor': 'end' }, 'chart-label');
            tickLabel.textContent = currency(value);
            chartGroup.appendChild(tickLabel);
        }

        chartGroup.appendChild(createNode('line', { x1: 0, y1: innerHeight, x2: innerWidth, y2: innerHeight }, 'chart-axis'));
        chartGroup.appendChild(createNode('line', { x1: 0, y1: 0, x2: 0, y2: innerHeight }, 'chart-axis'));

        const groupWidth = innerWidth / chartData.length;
        const barWidth = Math.min(26, Math.max(10, groupWidth * 0.28));
        const pairGap = Math.max(6, groupWidth * 0.12);

        const animatedBars = [];

        chartData.forEach((item, index) => {
            const incomeValue = Number(item.income || 0);
            const expenseValue = Number(item.expense || 0);

            const groupCenter = index * groupWidth + groupWidth / 2;
            const incomeX = groupCenter - pairGap / 2 - barWidth;
            const expenseX = groupCenter + pairGap / 2;

            const incomeTargetH = (incomeValue / roundedMax) * innerHeight;
            const expenseTargetH = (expenseValue / roundedMax) * innerHeight;

            const incomeBar = createNode(
                'rect',
                {
                    x: incomeX,
                    y: innerHeight,
                    width: barWidth,
                    height: 0,
                    rx: 6,
                    ry: 6,
                },
                'chart-bar-income'
            );

            const expenseBar = createNode(
                'rect',
                {
                    x: expenseX,
                    y: innerHeight,
                    width: barWidth,
                    height: 0,
                    rx: 6,
                    ry: 6,
                },
                'chart-bar-expense'
            );

            incomeBar.setAttribute('fill', 'url(#incomeGradient)');
            expenseBar.setAttribute('fill', 'url(#expenseGradient)');

            incomeBar.addEventListener('mousemove', (event) => showTooltip(event, item.name, 'Income', incomeValue));
            incomeBar.addEventListener('mouseleave', hideTooltip);
            expenseBar.addEventListener('mousemove', (event) => showTooltip(event, item.name, 'Expense', expenseValue));
            expenseBar.addEventListener('mouseleave', hideTooltip);

            chartGroup.appendChild(incomeBar);
            chartGroup.appendChild(expenseBar);

            const categoryLabel = createNode(
                'text',
                {
                    x: groupCenter,
                    y: innerHeight + 18,
                    'text-anchor': 'middle',
                },
                'chart-category-label'
            );
            categoryLabel.textContent = String(item.name || '').length > 10 ? `${String(item.name).slice(0, 9)}…` : String(item.name || '');
            chartGroup.appendChild(categoryLabel);

            animatedBars.push({ bar: incomeBar, target: incomeTargetH });
            animatedBars.push({ bar: expenseBar, target: expenseTargetH });
        });

        const defs = createNode('defs');
        const incomeGradient = createNode('linearGradient', { id: 'incomeGradient', x1: '0%', y1: '0%', x2: '0%', y2: '100%' });
        incomeGradient.appendChild(createNode('stop', { offset: '0%', 'stop-color': '#4ade80' }));
        incomeGradient.appendChild(createNode('stop', { offset: '100%', 'stop-color': '#16a34a' }));

        const expenseGradient = createNode('linearGradient', { id: 'expenseGradient', x1: '0%', y1: '0%', x2: '0%', y2: '100%' });
        expenseGradient.appendChild(createNode('stop', { offset: '0%', 'stop-color': '#fb7185' }));
        expenseGradient.appendChild(createNode('stop', { offset: '100%', 'stop-color': '#e11d48' }));

        defs.appendChild(incomeGradient);
        defs.appendChild(expenseGradient);
        svg.prepend(defs);

        const duration = 800;
        const start = performance.now();
        const easeOutCubic = (t) => 1 - (1 - t) ** 3;

        const animate = (time) => {
            const progress = Math.min(1, (time - start) / duration);
            const eased = easeOutCubic(progress);

            animatedBars.forEach(({ bar, target }) => {
                const heightNow = target * eased;
                const yNow = innerHeight - heightNow;
                bar.setAttribute('height', `${heightNow}`);
                bar.setAttribute('y', `${yNow}`);
            });

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    };

    renderChart();
    window.addEventListener('resize', renderChart);
});