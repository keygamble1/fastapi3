<script>
  import moment from 'moment/min/moment-with-locales';
  import { link } from 'svelte-spa-router';
  import fastapi from "../lib/api";
  import { is_login, keyword, page } from "../lib/store";
  
  moment.locale('ko')
    // url을 호출시 그에해당하는 svelte파일이 렌더링됨
    let question_list=[]
    let size=10
    let total=0
    let kw=''
    $:total_page=Math.ceil(total/size)
    // api호출로인해 변하면 실시간으로 변해짐 굳이
    // $: javascript안에서적용된 변수를 바로 가져와서 쓰는거라고보면됨 새로운변수
    // 먼저선언해줘야함 파이썬이랑다름
    function get_question_list(){
      let params={
        // 이건 맨처음에 parameter를 쓰는거라서 넣어야되는것
        // Detail경우에는 여기서 이미 정의된 question_id를 갔다쓰는거라서 params를 굳이 정의안해도됨

        page:$page,
        // _page=인자
        // 변수:형태
        size:size,
        keyword:$keyword,
      }

      fastapi('get','/api/question/list',params,
      // get에서 params를 생략하는게아닌 그냥 {}쓰는거고
      // 필요할때는 params를 추가시켜준다
        (json)=>{
          // get을 넣었을경우 queryparameter에 다떠버리니까 그 queryparameter를 가져와서
          // 각 형식에맞게 넣어버리는것임 paramaeter에 맞춰서
          // get이아닐경우 params을 json형태로해서 넣어버리는거
          question_list=json.question_list
          total=json.total
          kw=$keyword
          // 유지하고싶은걸 json에 업데이트함
          // $:$page, $keyword, get_question_list()
          // 이럴경우 page keyword 감지하면 get_question_list를
        }
      )
    }
    // page변경시 get_quesiton_list도 다시호출하라
    // $:재호출기호라는뜻

    // 하나면상관없는데 두개이상ㅅ부터는 해야함
    $:$page,$keyword,get_question_list()
    // 여기에 변수가없거나 새로 변수를 정의할때나 새로고침할때 $를 쓴다고보자
  </script>
  <div
    class="container my-3"
  >
      <div class="row my-3">
        <div class="col-6">
          <a use:link href="/question-create" class="btn btn-primary {$is_login ? '' :'disabled'}">질문등록</a>

        </div>
        <div class="col-6">
          <div class="input-group">
            <input type="text" class="form-control" bind:value={kw}>
            <button class="btn btn-outline-secondary" on:click={()=>{$keyword=kw,$page=0}} >
              찾기
            </button>
            
          </div>
        </div>
      </div>
      <table
        class="table"
      >
        <thead>
          <tr class="text-center table-dark">
            <th >번호</th>
            
            <th style="width:50% ;">제목</th>
            <th> 글쓴이</th>
            <th >작성일시</th>
          </tr>
        </thead>
        <tbody>
          <!--  뒤에나오면 인덱스 -->
          {#each question_list  as question,i}
          
          <tr class="text-center">
            <td >{total-($page*size)-1}</td>
            <td class="text-start">
              <a use:link href="/detail/{question.id}">{question.subject}</a>
              {#if question.answers.length >0}
              <span class="text-danger small mx-2">{question.answers.length}</span>
             {/if}
             <!-- 색따로 크기따로 -->
            </td>
            <td>{question.user ? question.user.username:""}</td>
            <td >{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
          </tr>
        {/each}
        </tbody>
      </table>
        <ul
          class="pagination justify-content-center   "
        >
          <li class="page-item {$page <= 0 &&  'disabled'}">
            <!-- 매개변수가들어갈시 그냥 자동으로버튼클릭되기때문에 ()=>로써줘야함 
             매개변수없으면참조지만 매개변수있으면 곧바로실행임 -->
            <button class="page-link" on:click="{()=>$page--}">이전 
            </button>
          </li>
          {#each Array(total_page) as _,loop_page }
          {#if loop_page>=$page-5 && loop_page<=$page+5}
          
          <!-- _는 배열객체 따로 변수안사용하겠따라는뜻 -->
          <li class="page-item {loop_page === $page &&  'active'}">
            <!-- 매개변수가들어갈시 그냥 자동으로버튼클릭되기때문에 ()=>로써줘야함 
             매개변수없으면참조지만 매개변수있으면 곧바로실행임 -->
            <button class="page-link" on:click="{()=>$page=loop_page}">{loop_page+1}
            </button>
          </li>
          {/if}
          {/each}
          <li class="page-item {$page >= total_page-1 &&  'disabled'}">
            <!-- 매개변수가들어갈시 그냥 자동으로버튼클릭되기때문에 ()=>로써줘야함 
             매개변수없으면참조지만 매개변수있으면 곧바로실행임 -->
            <button class="page-link" on:click="{()=>$page++}">다음
            </button>
          </li>
          


         
        </ul>
      
      
     
    </div>
    
  

