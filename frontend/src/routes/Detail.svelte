<script>
  import { marked } from 'marked';
  import moment from 'moment';
  import { link, push } from 'svelte-spa-router';
  import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";
  import { is_login, username } from '../lib/store';
 moment.locale('ko')
    export let params={}
    // get에서 question_detail은 그냥 Detail svelte로 바로가서그런거
    // quesiton/list는 매개변수를 받아서 params에 써야되는것
    let question_id=params.question_id
    // question은 answer이없을수도있거나 voter가 없을수도있기때문에
    // 명식적으로 해야함
    // 하지만 answers는 question이 있으면 기본적으로다 포함이 되어있기때문에 voter:[] 기본값이 있다면
    // 굳이 선언또안해줘도됨
    // :question app에서 받는거임
    let question={answers:[],voter:[],content:''}
    // question.answers를 하고싶으면 이렇게
    // quesiton.answers가능
    let error={detail:[]}
    // error.detail을 하고싶으면 이렇게
    // error.detail가능
    let content=""
    // 딕셔너리로 저장하라
    function get_question(){
        fastapi('get',"/api/question/detail/"+question_id,{},
            (json)=>{
                question=json
                // 검증하라고보내는거
            }
        )
    }
    get_question()
    
    function post_answer(event){
        event.preventDefault()
        // submit눌릴경우 자동전송 방지
        // 로컬로처리해서 폼데이터를 서버로넘기는게아닌 그냥 프론트엔드에서 처리가가능하기때문
       let url="/api/answer/create/"+question_id
    //    notfound뜨면 url이 잘못된거임
       let params={
            content:content
            // bind된 content가 지금 ㅜ이에있어서 그걸 가져와서 params에 넣음
       }
    //    params는 options body에 추가되서 갱신될것 javascript만되기때문에 params저형태로
       fastapi('post',url,params,
            (json)=>{
                content=''
                // 응답된 json을 가져옴
                error={detail:[]}
                get_question()
            },
            (err_json)=>{
                error=err_json
            }
        // successcallback=(json)=>{content='' getquesiton}
        // 저위에 두개가 모두 콜백함수
        // successcallback은 인자를 전달하는 콜백함수 (json)=>{content} 이건 함수를 전달받아 실행하는함수
        // 라고보면됨 왔다갔다하는거
        // 다른곳에 함수를 보내고 거기서 실행될시 여기서 또함수를 이동시켜버림
        // 한 함수가 다른함수내에서 실행하며 왔다갔다 한다는게 원래 말이안되는데 이건가능


       )
    //    새롭게 url을 만드는것 let url=
    }
    function delete_quesiton(question_id){
        if(window.confirm('정말삭제?')){
            let url="/api/question/delete"
            let params={
                question_id:question_id
            }
            fastapi('delete',url,params,
                (json)=>{
                    push('/')
                },
                (err_json)=>{
                    error=err_json
                }
            )
        }
    }
    function delete_answer(answer_id){
        if(window.confirm('정말삭제?')){
            let url="/api/answer/delete"
            let params={
                answer_id:answer_id
            }
            fastapi('delete',url,params,
                (json)=>{
                    get_question()
                },
                (err_json)=>{
                    error=err_json
                }
            )
        }
    }
    function vote_question(_question_id){
        if(window.confirm('정말추천?')){
            let url="/api/question/vote"
     
            let params={
                question_id:_question_id
            }
        fastapi('post',url,params,
            (json)=>{
                get_question()
                // export let params에서 나온 question_id를 계속가지고있어서 가능
            },
            (err_json)=>{
                error=err_json
            }
        )
    }
}
function vote_answer(_answer_id){
        if(window.confirm('정말추천?')){
            let url="/api/answer/vote"
     
            let params={
                answer_id:_answer_id
            }
        fastapi('post',url,params,
            (json)=>{
                get_question()
                // export let params에서 나온 answer_id를 계속가지고있어서 가능
            },
            (err_json)=>{
                error=err_json
            }
        )
    }
}

</script>
<div
    class="container"
>
    <h2 class="border-bottom py-2">{question.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" >
                {@html marked.parse(question.content)}</div>
            <div class="d-flex justify-content-end">
                {#if question.modify_date}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{question.user ? question.user.username : ""}</div>
                    <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{question.user ? question.user.username : ""}</div>
                    <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>

            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary" 
                on:click="{vote_question(question.id)}"> 
                    추천
                    <span class="badge rounded-pill bg-success" >{question.voter.length}</span>
                </button>
                {#if question.user && $username===question.user.username}
                    <a use:link href="/question-modify/{question.id}"
                    class="btn btn-sm btn-outline-secondary">수정</a>
                <button class="btn btn-sm btn-outline-secondary"
                on:click={()=>delete_quesiton(question.id)}>삭제</button>
                    {/if}
                
            </div>
        </div>
    </div>
    <button class="btn btn-secondary" on:click="{()=>push('/')}">
        목록으로
    </button>
    <!--답변목록 -->
    <h5 class="border-bottom my-3 py-2">{question.answers.length}개있음</h5>
    {#each question.answers as answer }
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" >
                {@html marked.parse(answer.content)}</div>
            <div class="d-flex justify-content-end">
                              {#if answer.modify_date}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{answer.user ? answer.user.username : ""}</div>
                    <div>{moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                {/if}
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{answer.user ? answer.user.username : ""}</div>
                    <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                <button class="btn btn-sm btn-outline-secondary" 
                on:click="{vote_answer(answer.id)}"> 
                    추천
                    <span class="badge rounded-pill bg-success" >{answer.voter.length}</span>
                </button>
                {#if answer.user && $username===answer.user.username}
                    <a use:link href="/answer-modify/{answer.id}"
                    class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-secondary"
                     on:click={()=>delete_answer(answer.id)}>삭제</button>
               
                    {/if}
                
            </div>
            
 
        </div>
    </div>
    
    {/each}
    <Error error={error}/>
    <form  method="post" class="my-3">
        <div class="mb-3">
            <textarea bind:value={content}
            disabled={$is_login ? '' : 'disabled'}
             rows="10" class="form-control"></textarea>
        <!-- {}그냥 이건 변수고 "{}"는 함수를 뜻함 -->
        </div>
        <input type="submit" value="답변등록" class="btn btn-primary {$is_login ? '' : 'disabled'}" on:click="{post_answer}">
    </form>
    
</div>
