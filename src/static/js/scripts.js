function generatePackageNumber() {
    fetch('/generate')
        .then(response => response.json())
        .then(data => {
            document.getElementById('random-package-number').textContent = data.package_number;
        });
}
