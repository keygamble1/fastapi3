<script>
  import { push } from 'svelte-spa-router';
  import Error from "../components/Error.svelte";
  import fastapi from "../lib/api";
  import { access_token, is_login, username, } from '../lib/store';
  let error={detail:[]}
  let login_username=''
  let login_password=''
  function login(event){
    event.preventDefault()
    let url="/api/user/login"
    let params={
        username:login_username,
        password:login_password
    }
    fastapi('login',url,params,
        (json)=>{
            // access_token localstorage에 저장하는거임
            $access_token=json.access_token
            $username=json.username
            $is_login=true
            push('/')
        }
        ,
        (err_json)=>{
            error=err_json
        }
    )
    // 로그인수행시 application/x-www-form-urlencoded 이타입으로 사용해버림

    // 보통서버에 폼제출하고 응답안기다린상태에서 새로고침함 이걸방지하기위해
    // event.preventdefault쓰고, 프론트엔드에서 새로고침을 안시켜서 비동기나 여러가지를 처리한
    // 새로고침하는순간 데이터만 전송하고 추가적으로 api추가요청등 비동기로 처리를 못함
    // 응답에따라 처리하기위해 default로 기본동작(새로고침)막고 비동기로 응답에따라처리해버림

    
  }
</script>
<div
    class="container"
>   
    <h5 class="border-bottom pb-2">로그인</h5>
    <Error error={error}/>
    <form  method="post">
        <div class="mb-3">
            <label for="username">사용자이름</label>
            <input type="text" class="form-control" id="username" bind:value={login_username}>
        </div>
        <div class="mb-3">
            <label for="password">비밀번호</label>
            <input type="text" class="form-control" id="password" bind:value={login_password}>
        </div>
        <button type="submit" class="btn btn-primary" on:click="{login}">로그인</button>

    </form>
</div>
