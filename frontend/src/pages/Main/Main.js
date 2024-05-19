//PageOne.js
import React from "react";

import { Link } from 'react-router-dom';
import Navbarboot from "../../components/Header/Navbarboot";


const Main = () => {
  return (
  <>
    <Navbarboot></Navbarboot>
    <div>
      <p>메인홈입니다. 환영합니다.</p>
      <button>
        <Link to="/Board">게시판으로 이동</Link>
      </button>
    </div>
    </>
  );
};

export default Main;