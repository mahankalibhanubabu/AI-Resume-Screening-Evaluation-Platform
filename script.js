const form = document.getElementById("resumeForm");

const fileInput = document.getElementById("resume");

const fileName = document.getElementById("fileName");

const status = document.getElementById("status");

fileInput.addEventListener("change", () => {

    if(fileInput.files.length>0){

        fileName.innerHTML="Selected File : "+fileInput.files[0].name;

    }

    else{

        fileName.innerHTML="No file selected";

    }

});

form.addEventListener("submit",(e)=>{

    e.preventDefault();

    const candidateName=document.getElementById("candidateName").value.trim();

    const email=document.getElementById("email").value.trim();

    const jobRole=document.getElementById("jobRole").value.trim();

    const resume=fileInput.files[0];

    if(candidateName==="" || email==="" || jobRole===""){

        status.className="error";

        status.innerHTML="Please fill all fields.";

        return;

    }

    if(!resume){

        status.className="error";

        status.innerHTML="Please upload a resume.";

        return;

    }

    status.className="loading";

    status.innerHTML="Submitting...";

    /*
    Next Step (Flask/FastAPI)

    const formData = new FormData();

    formData.append("candidateName", candidateName);
    formData.append("email", email);
    formData.append("jobRole", jobRole);
    formData.append("resume", resume);

    fetch("http://127.0.0.1:5000/upload",{
        method:"POST",
        body:formData
    })
    .then(res=>res.json())
    .then(data=>{
        status.className="success";
        status.innerHTML=data.message;
    })
    .catch(err=>{
        status.className="error";
        status.innerHTML="Something went wrong.";
    });
    */

    setTimeout(()=>{

        status.className="success";

        status.innerHTML="Frontend completed successfully. Ready for Flask/FastAPI integration.";

    },1500);

});