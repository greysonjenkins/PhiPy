document.addEventListener('DOMContentLoaded', () => {
    // ... other code ...

    generateTreeBtn.addEventListener('click', async () => {
        console.log('Generate tree button clicked');
        if (sentences.length === 0) {
            alert('Please add at least one sentence.');
            return;
        }

        const options = {
            showLineNumbers: document.getElementById('show-line-numbers').checked,
            circleAtomic: document.getElementById('circle-atomic').checked,
            markClosedBranches: document.getElementById('mark-closed-branches').checked,
            showDecompositionRule: document.getElementById('show-decomposition-rule').checked
        };

        try {
            console.log('Sending request to server:', { sentences, options });
            const response = await fetch('/generate_tree', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sentences, options }),
            });

            console.log('Received response from server');
            const data = await response.json();

            if (data.error) {
                console.error('Error from server:', data.error);
                alert(`Error: ${data.error}`);
                return;
            }

            console.log('Tree data received:', data.tree);

            // Visualize the tree using d3-graphviz
            d3.select("#tree-visualization").graphviz()
                .renderDot(data.tree);

            console.log('Tree visualization complete');
        } catch (error) {
            console.error('Fetch error:', error);
            alert(`An error occurred: ${error.message}`);
        }
    });
});