
(function () {
    "use strict";

    // ==========================================
    // ROHIL NEXTGEN - IMAGE PERFORMANCE OPTIMIZER
    // ==========================================

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

    // ------------------------------------------
    // 1. Convert image paths to WebP paths
    // ------------------------------------------

    function optimizeImagePath(originalPath) {
        if (!originalPath) return originalPath;

        try {
            const url = new URL(originalPath, document.baseURI);

            // Keep external images unchanged
            if (url.origin !== window.location.origin) {
                return originalPath;
            }

            let path = url.pathname;

            // Only convert JPG, JPEG and PNG
            if (!IMAGE_EXTENSIONS.test(path)) {
                return originalPath;
            }

            for (const folder of IMAGE_FOLDERS) {
                if (path.includes(folder.oldFolder)) {
                    path = path.replace(
                        folder.oldFolder,
                        folder.newFolder
                    );

                    path = path.replace(
                        IMAGE_EXTENSIONS,
                        ".webp"
                    );

                    url.pathname = path;

                    return url.pathname + url.search + url.hash;
                }
            }

            return originalPath;

        } catch (error) {
            console.warn(
                "Image path error:",
                originalPath,
                error
            );

            return originalPath;
        }
    }

    // ------------------------------------------
    // 2. Optimize src and srcset paths
    // ------------------------------------------

    function optimizeSrcset(srcset) {
        if (!srcset) return srcset;

        return srcset
            .split(",")
            .map(candidate => {
                const parts = candidate.trim().split(/\s+/);

                if (!parts[0]) return candidate;

                parts[0] = optimizeImagePath(parts[0]);

                return parts.join(" ");
            })
            .join(", ");
    }

    function optimizeImageSources(element) {

        // Optimize src
        const oldSrc = element.getAttribute("src");

        if (oldSrc) {
            const newSrc = optimizeImagePath(oldSrc);

            if (newSrc !== oldSrc) {
                element.setAttribute("src", newSrc);
            }
        }

        // Optimize srcset
        const oldSrcset = element.getAttribute("srcset");

        if (oldSrcset) {
            const newSrcset = optimizeSrcset(oldSrcset);

            if (newSrcset !== oldSrcset) {
                element.setAttribute("srcset", newSrcset);
            }
        }
    }

    // ------------------------------------------
    // 3. Optimize image loading
    // ------------------------------------------

    function optimizeImageLoading(img) {

        // Do not override existing decoding settings
        if (!img.hasAttribute("decoding")) {
            img.setAttribute("decoding", "async");
        }

        // Preserve explicitly configured loading
        if (img.hasAttribute("loading")) {
            return;
        }

        // Respect images explicitly marked as important
        if (
            img.hasAttribute("data-no-lazy") ||
            img.hasAttribute("data-lcp") ||
            img.getAttribute("fetchpriority") === "high"
        ) {
            img.setAttribute("loading", "eager");
            return;
        }

        // Lazy load only images below the initial viewport
        const rect = img.getBoundingClientRect();

        if (
            rect.width > 0 &&
            rect.height > 0 &&
            rect.top > window.innerHeight
        ) {
            img.setAttribute("loading", "lazy");
        }
    }

    // ------------------------------------------
    // 4. Process individual images
    // ------------------------------------------

    function processImage(img) {

        optimizeImageSources(img);

        optimizeImageLoading(img);
    }

    // ------------------------------------------
    // 5. Process image and picture elements
    // ------------------------------------------

    function processElement(element) {

        if (element.matches("img")) {
            processImage(element);
        }

        if (element.matches("source")) {
            optimizeImageSources(element);
        }

        element.querySelectorAll("img, source").forEach(item => {

            if (item.matches("img")) {
                processImage(item);
            } else {
                optimizeImageSources(item);
            }

        });
    }

    function optimizeImages(root = document) {

        root.querySelectorAll("img, source").forEach(element => {

            if (element.matches("img")) {
                processImage(element);
            } else {
                optimizeImageSources(element);
            }

        });
    }

    // ------------------------------------------
    // 6. Handle dynamically added images
    // ------------------------------------------

    function observeDynamicImages() {

        const observer = new MutationObserver(mutations => {

            mutations.forEach(mutation => {

                mutation.addedNodes.forEach(node => {

                    if (node.nodeType === Node.ELEMENT_NODE) {
                        processElement(node);
                    }

                });

            });

        });

        observer.observe(document.documentElement, {
            childList: true,
            subtree: true
        });

    }

    // ------------------------------------------
    // 7. Initialize optimizer
    // ------------------------------------------

    function initializeOptimizer() {

        optimizeImages();

        observeDynamicImages();

        console.log(
            "Rohil NextGen image optimization initialized."
        );

    }

    if (document.readyState === "loading") {

        document.addEventListener(
            "DOMContentLoaded",
            initializeOptimizer,
            { once: true }
        );

    } else {

        initializeOptimizer();

    }

})();
