# シカの季節位相と滞在調整：同一個体・年固定効果による追加解析

2026-11-22 / 公表済み原データの探索的二次解析 / 元原稿・mainは未変更

## 結果

**同じ個体の年際変化を比べても、季節に対して遅く出発した年ほど途中の滞在が短い関連が残った。**

原データの反復測定部分は38個体・100個体年、2011–2020年のうち8観測年。
個体固定効果と年固定効果を同時に調整した係数は、出発位相1日あたり
**−0.689113日**、個体クラスタ・ブートストラップ95%区間は
**[−0.815051, −0.572581]日**だった。

出発時の季節位相が10日遅い場合に換算すると、滞在は平均6.89日短い関連
（95%区間：5.73–8.15日短縮）である。これは同じ個体についての条件付き平均関係であり、
全個体がそれぞれ同じ係数を持つことや、出発を操作すれば同量の変化が起きることを意味しない。

## 同一の100行での比較

| 比較 | 出発位相1日あたりの滞在日数の係数 |
|---|---:|
| 個体・年を調整しない回帰 | −0.486952 |
| 年固定効果を調整 | −0.617077 |
| **個体＋年固定効果（主解析）** | **−0.689113** |

したがって、固定的な個体差を除くと関連が消えるという結果ではなかった。
個体の恒常的な移動特性と、すべての個体に共通する年ごとの差だけでは、
この標本内の位相と滞在の関係を説明しきれない。
最初の2行は同一標本の記述的参照値であり、別々の独立した肯定結果とは数えない。

## 年を一つずつ除外した感度分析

| 除いた年 | 反復個体数 | 個体年数 | 係数（日／位相日） |
|---|---:|---:|---:|
| 2011 | 34 | 92 | −0.691248 |
| 2012 | 34 | 92 | −0.691248 |
| 2014 | 36 | 95 | −0.710044 |
| 2016 | 35 | 91 | −0.706836 |
| 2017 | 29 | 70 | −0.802203 |
| 2018 | 25 | 59 | −0.603914 |
| 2019 | 32 | 75 | −0.514595 |
| 2020 | 35 | 82 | −0.695348 |

8通りすべてで負の係数が残った。これは方向の感度分析であり、
8通りの区間がすべて0を除くという検定結果ではない。
2011と2012をそれぞれ除くと、初期コホートは反復比較に使えなくなるため、
残る標本と推定値が同じになる。

## データとモデル

原資料：Ortega AC et al. (2023), *Migrating mule deer compensate en route for
phenological mismatches*, Nature Communications 14:2008.
[原論文](https://doi.org/10.1038/s41467-023-37750-z)
／[原著全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC10086060/)

Source Dataファイル：41467_2023_37750_MOESM4_ESM.xlsx、629,058 bytes。
SHA256：2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364。
公式配布ファイルを再取得し、既存解析のハッシュと一致することを確認した。

- 位相シートは Fig1a,b;Fig3;SFig2;STables1,6、行動シートは Fig4d,4e;SFig4 のA:Gブロック。
- 原データ152個体年・72個体から、滞在期間が利用可能な127個体年・65個体を確認。
- BBMM品質条件により原著で欠測となる25行は0に補完しない。真の0日滞在15行は保持。
- 完全ケースが1年だけの27個体を主解析から除き、100個体年・38個体とした。
  この反復部分標本にも真の0日滞在11行が含まれる。
- id_yrの一意性、両シートのキー集合一致、個体年表記とyear列の一致を検証。

主式：StopoverDays_it = animal_i + year_t + beta * DFP_Start_it + error_it。
DFP_Startは正ほど植物の緑化ピークに対して遅い。年次の植物季節から事後に再構成した
位相であり、動物が出発時点で知っていた情報を測る変数ではない。

不均衡パネルなので、単純に個体平均と年平均を一度ずつ差し引く方法は用いない。
個体効果を除去した後、同様に残差化した年ダミーの列空間へ正確に射影する。
固定効果除去後の出発位相RMSは13.5967日、主モデルの残差自由度は55。

個体を丸ごと再抽出するブートストラップ10,000反復、seed=20261122。
重複して引いた個体履歴には別ラベルを与え、各反復で個体・年効果を再推定した。
10,000反復すべてが推定可能だった。区間は観測された年に条件づけた不確実性である。

## 係数計算前の設計修正

初期設計は個体×年のグラフに1連結成分を要求したため、構造確認段階で不成立と判定した。
実際には初期4個体・8行と後期34個体・92行の2成分だった。この元の判定は保存している。

固定効果の列空間のrankは38+8−2=44であり、残差化した出発位相に変動があるため、
共通傾きは識別できる。独立した統計レビュー後、**新しい係数・区間を見る前に**、
連結性を必要条件から構造診断へ変更した。行・変数・モデル・ブートストラップは変えていない。
これは探索的設計修正であり、当初設計の確認的成功とは呼ばない。

識別に使う残差位相の平方和の97.962%は後期コホートに由来する。
全8年間を同じ個体で追跡した結果や、独立2集団での再現とは解釈しない。
[修正理由と計算前の記録](PAYOFF_B_ORTEGA_WITHIN_ANIMAL_DESIGN_20261122.md)

## 新たに確認したことと主張の上限

今回追加したのは、既報の補償関連が、個体効果と出発位相の独立性を仮定しない
固定効果モデルでも残るという頑健性確認である。原著は補償そのものを既に報告しており、
個体・年のランダム切片を持つモデルも使用している。
「個体差を初めて調整した」「補償を新発見した」とは主張しない。

滞在は旅程の時間配分の一部であるため、この関連だけで情報の感知、学習、能動制御の
因果効果、修正機会の閾値や適応度の改善は識別できない。個体ごと・年ごとに変わる環境や
経路の違いも残り得る。出発位相自体の測定誤差も補正していない。

当初検討した「到着位相を全旅程速度で予測」は、速度の定義が距離÷全旅程日数であり、
到着情報を含むため実行前に退けた。到着位相、全旅程速度、総移動期間、事後の補償分類は
今回の主解析の説明変数に使用していない。

## English result paragraph

In an exploratory reanalysis of the published Ortega et al. (2023) source data,
we retained 100 complete animal-years from 38 repeatedly observed mule deer.
After adjusting for individual and year fixed intercepts, later departure phase
was associated with shorter stopover duration (beta = -0.689 days per phase day;
animal-cluster bootstrap 95% interval -0.815 to -0.573). The association remained
negative in all eight leave-one-year-out analyses (range -0.802 to -0.515).
Thus, the previously reported compensation association persisted after removing
stable individual differences and common year effects. This is a conditional
within-individual time-allocation association, not an independent discovery of
compensation or an identification of information use or causal feedback.

## Reproduction and verification

The coefficient-blind code and amended contract were committed at b31d194 before
the new empirical fit. The original design and structural failure remain at
eaf8d99 and 72a5ad4. The result file records the exact source and contract digests.

Install the repository's test and empirical dependencies, download the original
XLSX from the URL in the contract, and run:

```bash
python scripts/payoff_b_ortega_within_animal.py \
  --source /path/to/41467_2023_37750_MOESM4_ESM.xlsx \
  --contract data/payoff_b_ortega_within_animal_contract_v2_20261122.json \
  --output outputs/payoff_b_ortega_within_animal_result_20261122.json
```

The dedicated tests cover missing versus zero durations, duplicate and unmatched
source keys, exact unbalanced fixed effects, absent identifying variation,
whole-animal resampling and disconnected-component normalization invariance.
An independent full categorical-design regression with a pivoted-QR nuisance
basis reproduced the primary coefficient to numerical precision.

Machine-readable result:
[result JSON](../data/payoff_b_ortega_within_animal_result_20261122.json).
Original raw rows, animal IDs and source workbook are not committed.
