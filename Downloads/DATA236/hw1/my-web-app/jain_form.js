const validateForm = () => {
    const content = document.getElementById("content").value.trim();
    const termsChecked = document.getElementById("terms").checked;

    if (content.length <= 25) {
        alert("Blog content should be more than 25 characters");
        return false;
    }

    if (!termsChecked) {
        alert("You must agree to the terms and conditions");
        return false;
    }

    return true;
};

const blogCounter = (() => {
    let count = 0;
    return () => ++count;
    })();

document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    const title = document.getElementById("title").value.trim();
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const content = document.getElementById("content").value.trim();
    const category = document.getElementById("category").value;
    const termsChecked = document.getElementById("terms").checked;

    const blogData = {
        title,
        name,
        email,
        content,
        category,
        agreedToTerms: termsChecked,
        timestamp: new Date().toISOString()
    };

    const jsonBlogData = JSON.stringify(blogData, null, 2);
    console.log("String Blog Data:", jsonBlogData);

    const parsedBlogData = JSON.parse(jsonBlogData);
    console.log("Json Blog Data:", parsedBlogData);

    const { title: parsedTitle, email: parsedEmail } = parsedBlogData;
    console.log("Title:", parsedTitle);
    console.log("Email:", parsedEmail);

    const currentCount = blogCounter();
    const updatedBlog = {...parsedBlogData, id: `blog-${currentCount}`, submissionDate: new Date().toLocaleString()};

    console.log("Blog Counter:", currentCount);
    console.log("Updated Blog:", updatedBlog);

    //document.querySelector("form").reset();
});