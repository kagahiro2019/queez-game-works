// ========================================
// AI-husband Prototype
// Chat UI
// ========================================


// ----------------------------------------
// HTML要素を取得
// ----------------------------------------

const messageInput = document.querySelector(
  ".chat-input textarea"
);

const sendButton = document.querySelector(
  ".chat-input button:last-child"
);

const chatMessages = document.querySelector(
  ".chat-messages"
);


// ----------------------------------------
// オートスクロール
// ----------------------------------------

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}


// ----------------------------------------
// ユーザーの吹き出しを追加
// ----------------------------------------

function addUserMessage(message) {
  const messageRow = document.createElement("div");

  messageRow.classList.add(
    "message-row",
    "user"
  );

  const messageBubble = document.createElement("div");

  messageBubble.classList.add(
    "message-bubble"
  );

  messageBubble.textContent = message;

  messageRow.appendChild(messageBubble);

  chatMessages.appendChild(messageRow);

  scrollToBottom();
}


// ----------------------------------------
// AI_Yatoの吹き出しを追加
// ----------------------------------------

function addYatoMessage(data) {
  const yatoRow = document.createElement("div");

  yatoRow.classList.add(
    "message-row",
    "yato"
  );


  // ----------------------------------------
  // 夜斗アイコン
  // ----------------------------------------

  const yatoIcon = document.createElement("img");

  yatoIcon.src =
    "Asset/AI_manager_100_010_010.png";

  yatoIcon.alt = "夜斗";

  yatoIcon.classList.add(
    "yato-icon"
  );

  // Pythonから返ってきた感情IDを保持
  yatoIcon.dataset.emotion =
    data.emotion_ID;


  // ----------------------------------------
  // 吹き出し
  // ----------------------------------------

  const yatoBubble =
    document.createElement("div");

  yatoBubble.classList.add(
    "message-bubble",
    `emotion-${data.emotion_ID}`
  );

  yatoBubble.textContent =
    data.message;


  // ----------------------------------------
  // 画面へ追加
  // ----------------------------------------

  yatoRow.appendChild(yatoIcon);
  yatoRow.appendChild(yatoBubble);

  chatMessages.appendChild(yatoRow);

  scrollToBottom();
}


// ----------------------------------------
// メッセージ送信
// ----------------------------------------

async function sendMessage() {

  // 入力された文章を取得
  const message =
    messageInput.value.trim();


  // 空欄なら送信しない
  if (message === "") {
    return;
  }


  // ----------------------------------------
  // ユーザーのメッセージを表示
  // ----------------------------------------

  addUserMessage(message);


  // ----------------------------------------
  // 入力欄を空にする
  // ----------------------------------------

  messageInput.value = "";


  // ----------------------------------------
  // Pythonバックエンドへ送信
  // ----------------------------------------

  try {

    const response = await fetch("https://queez-game-works-git-576440453459.europe-west1.run.app/chat", 
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          message: message
        })
      }
    );


    // ----------------------------------------
    // HTTPエラー確認
    // ----------------------------------------

    if (!response.ok) {
      throw new Error(
        `HTTP Error: ${response.status}`
      );
    }


    // ----------------------------------------
    // PythonからJSON取得
    // ----------------------------------------

    const data = await response.json();

    console.log(
      "AI_Yato Response:",
      data
    );


    // ----------------------------------------
    // 夜斗の返答を表示
    // ----------------------------------------

    addYatoMessage(data);


  } catch (error) {

    console.error(
      "AI_Yato通信エラー:",
      error
    );

  }
}


// ----------------------------------------
// 「送信」ボタン
// ----------------------------------------

sendButton.addEventListener(
  "click",
  sendMessage
);


// ----------------------------------------
// Enterキー
// ----------------------------------------

messageInput.addEventListener(
  "keydown",
  (event) => {

    // ----------------------------------------
    // 日本語IME変換中
    // ----------------------------------------

    if (event.isComposing) {
      return;
    }


    // ----------------------------------------
    // Shift + Enter は改行
    // ----------------------------------------

    if (
      event.key === "Enter" &&
      event.shiftKey
    ) {
      return;
    }


    // ----------------------------------------
    // Enterだけなら送信
    // ----------------------------------------

    if (event.key === "Enter") {

      event.preventDefault();

      sendMessage();
    }
  }
);