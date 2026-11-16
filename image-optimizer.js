(function () {
    "use strict";

    const IMAGE_FOLDERS = [
        {
            oldFolder: "/images/",
            newFolder: "/optimized-images/"
        },
        {
            oldFolder: "/gallery/",
            newFolder: "/optimized-gallery/"
        }
    ];

    const IMAGE_EXTENSIONS = /\.(jpg|jpeg|png)$/i;

    function optimizeImagePath(originalPath) {
        if (!originalPath) return originalPath;

        try {
            const url = new URL(originalPath, document.baseURI);

            // External images should remain unchanged
            if (url.origin !== window.location.origin) {
                return originalPath;
            }

            let path = url.pathname;

            if (!IMAGE_EXTENSIONS.test(path)) {
                return originalPath;
            }

            for (const folder of IMAGE_FOLDERS) {
                if (path.includes(folder.oldFolder)) {
                    path = path.replace(
                        folder.oldFolder,
                        folder.newFolder
                    );

                    path = path.replace(IMAGE_EXTENSIONS, ".webp");

                    url.pathname = path;

                    return url.pathname + url.search + url.hash;
                }
            }

            return originalPath;

        } catch (error) {
            console.warn("Image path error:", originalPath, error);
            return originalPath;
        }
    }

    function optimizeImages(root = document) {
        root.querySelectorAll("img").forEach(img => {
            const oldSrc = img.getAttribute("src");

            if (oldSrc) {
                const newSrc = optimizeImagePath(oldSrc);

                if (newSrc !== oldSrc) {
                    img.setAttribute("src", newSrc);
                }
            }
        });

        root.querySelectorAll("source").forEach(source => {
            const oldSrc = source.getAttribute("src");

            if (oldSrc) {
                const newSrc = optimizeImagePath(oldSrc);

                if (newSrc !== oldSrc) {
                    source.setAttribute("src", newSrc);
                }
            }
        });
    }

    // Optimize images when page loads
    optimizeImages();

    // Handle images added dynamically
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.matches("img, source")) {
                        const oldSrc = node.getAttribute("src");

                        if (oldSrc) {
                            const newSrc = optimizeImagePath(oldSrc);
                            if (newSrc !== oldSrc) {
                                node.setAttribute("src", newSrc);
                            }
                        }
                    }

                    optimizeImages(node);
                }
            });
        });
    });

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });

    console.log("Rohil NextGen image optimization initialized.");
})();
