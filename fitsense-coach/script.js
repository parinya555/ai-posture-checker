function showPlan(goal){

    const result = document.getElementById("result");
  
    if(goal === "lose"){
  
      result.innerHTML = `
        <h3>โปรแกรมลดน้ำหนัก</h3>
  
        <p>วิ่ง 30 นาที</p>
  
        <p>HIIT 15 นาที</p>
  
        <p>คุมอาหาร</p>
      `;
    }
  
    else if(goal === "muscle"){
  
      result.innerHTML = `
        <h3>โปรแกรมเพิ่มกล้าม</h3>
  
        <p>Weight Training</p>
  
        <p>กินโปรตีนสูง</p>
  
        <p>พักผ่อนให้เพียงพอ</p>
      `;
    }
  }