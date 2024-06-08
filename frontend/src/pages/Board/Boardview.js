import React, { useState, useEffect} from "react";
import Navbarboot from "../../components/Header/Navbarboot";
import axios from "axios";
import { useParams } from 'react-router-dom';
import {ApiURL} from '../../ApiURL/ApiURL';

function Boardview(props){
    const { idx } = useParams(); // /Board/view/:idx와 동일한 변수명으로 데이터를 꺼낼 수 있습니다.
    const [loading, setLoading] = useState(true);
    const [board, setBoard] = useState({});
    const getBoard = async () => {
        const resp = await (await axios.get(`${ApiURL.Boardview_get}`)).data;
        setBoard(resp.data);
        console.log(resp);
        setLoading(false);
      };
      useEffect(() => {
        getBoard();
      }, []);
      
    return(<>
        <div>
            <Navbarboot></Navbarboot>
        </div>
        <div>
            {console.log(typeof board)}
            {board.id}
        </div>
        <div>
            아이디 입력날짜 수정 삭제버튼
        </div>

        <div>본문</div>
        </>
    );
}

export default Boardview;