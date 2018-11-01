# porker-local-rule-
ポーカー(ローカルルール)

1.dealerがプレイヤーに5枚ずつカードを配る
2.playerが捨てるカードのリストを返す(公開される)
3.dealerが捨てたカードの枚数をplayerに配る
4.playerが'call'or'stay'を返す
5.dealerがもつカードデッキが5枚以下になれば捨てられたカードをデッキの戻しシャッフルする
※'call'が出てから一巡するまで2~5を繰り返す
6.全員の手札を公開し手札を評価、勝者を決める

<playerが用意する関数>
get_hand()...dealerからカードを受け取る
restore_cards()...捨てるカードリストを返す
respond()...新しい手札を見て'call'or'stay'を返す


<今後の改変事項>
チップをかける仕様の検討
