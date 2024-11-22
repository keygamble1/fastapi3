<script>
  
	import Router from 'svelte-spa-router';
	import Navigation from './components/Navigation.svelte';
	import AnswerModfiy from './routes/AnswerModfiy.svelte';
	import Detail from './routes/Detail.svelte';
	import Home from "./routes/Home.svelte";
	import QuestionCreate from './routes/QuestionCreate.svelte';
	import QuestionModify from './routes/QuestionModify.svelte';
	import UserCreate from './routes/UserCreate.svelte';
	import UserLogin from './routes/UserLogin.svelte';

	  
    const routes={
      '/':Home,
      '/detail/:question_id':Detail,
      // detail은 :quesiton_id를 params로 전달 얘만하는거
      '/question-create':QuestionCreate,
      // :question_id= params에 전달됨
      '/user-create':UserCreate,
      '/user-login':UserLogin,
      '/question-modify/:question_id':QuestionModify,
      '/answer-modify/:answer_id':AnswerModfiy
    }
  
</script>
<!-- app.svelte통해야 실행다가능 -->
<Navigation/>
<Router {routes}/>
<!-- 
  // svelte는 변수를 초기화먼저해줘야함
  // javascript 형식은 안해도된다고 false해놓음
  
  // fetch는 서버에 네트워크요청보내고 받아오는역할
  // 즉 fastapi의 url을 받고 얻을수있음
  // ajax에서 비동기적으로 받아오는것
  // fetch(url,options) url에요청보내고 [options]에 header나 mthod드을 지정가능
  // options에 없으면 get으로 되고 url로부터 다운로드됨
  // fetch는 네트워크 요청보내는동시에 프로미스반ㄴ환됨 반환되는 프로미스는 fetch()를 호출하는곳에서 또 받는다
  // 요청보내기->안기다리고 프로미스반환-> 서버에서 응답받은헤더를 이미 처리후 반환한 프로미스안에있는 response의 인스턴스와 함께이행 즉 미리 프로미스화된거+헤더랑 이행된다는것
  // 이건 아직 서버에서 body도착안하고 헤더만받았지만 요청 성공인지아닌지 확인가능
  // 문제및 존재x시 프로미스는 거부상태 이건 http propery로 확인 http 400이런걸로
  // 프로미스안 response에는 다양한메서드있음 response.text=>텍스트반환
  // response.json->json형태 파싱
  // response.formdata->formdata로 반환
  // response.text나 response.json둘중하나만 사용
  // 비동기는즉 읽고넘기고 읽고넘기고한다는뜻
// response => response.json()이거 자체가 콜백함수
// then(이거는 앞의 프로미스의 결과값=>결과값을바로 .json()하거나 .text()로 변환)
// response는 순차적으로 진행되는 스트림이라서 json(respose) 이렇게 간단하게안됨
//응답해더=content-type apllcation/json 으로 받고
//요청헤더 heades요옵션사용시 요청헤더 서ㅈ억나으 authentcation secret 이런건 제약조건 즉 http목적에맞게 사용가능
// get이외는 httpmethod(post등) 
// body는 요청본문으로 문자열(json), formdate blob이런거 URLSearchParams 데이터를 ww형태로 보내기위해쓰는데 요즘엔잘사용안함
// method,heades=contenttype,body=json의 문자열이라고보면됨 post요청은 본문이 문자일경우 기본 text/plan이라서
// json을 전송시 제대로된타입인 application/json으로 다 바꿔버려야함
// options에는 method,headers,body가들어가는데 이런것들은다 제약조건이라고봐야함 -->
