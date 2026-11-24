# PAYOFF-B：公開コウノトリGPSアーカイブの内部構造と時刻・個体の列を原本から確認

**2026-11-24｜公開CC0アーカイブの取得可能範囲・技術的スキーマの原資料監査。GPS個別イベント・座標・生存アウトカムは解析も公開もしていない。**

## 結論

Bontekoe et al. (2023, Proceedings B, DOI 10.1098/rspb.2023.1268) の対照・遅延・自然出発の原本GPS ZIPを、**全件をダウンロードせずHTTP 206 Rangeで部分取得**した。各群の大きなCSVについて、先頭ヘッダーの**26列がすべて一致**した。

| 原本アーカイブ | ZIPサイズ | CSV数 | 大きなCSVの展開後サイズ | 先頭ヘッダー |
|---|---:|---:|---:|---|
| 対照 | 289,189,615 bytes | 2 | 2,271,728,532 bytes | **26列、検証済み** |
| 遅延 | 297,340,370 bytes | 2 | 2,115,632,725 bytes | **26列、検証済み** |
| 自然出発 | 311,814,202 bytes | 1 | 2,268,167,309 bytes | **26列、検証済み** |

各原本の ZIP central directory は正しい構造だった（通常のDeflate method 8）。対照と遅延の2番目のCSVはそれぞれ**展開後176バイト**であり、先頭4KB以内に改行付きのCSVヘッダーが存在するという元の規則を満たさず、ヘッダー認定を保留した。したがって「5つのCSVすべてを解析可能と確認」とは言わない。**時刻・タグ・位置を記録する大きなCSVが3群に存在することは確認した。**

## 原本から確認できた主要26列

3群で同一の列名が存在する。フィールド例：

| 分野 | 原本の列名 |
|---|---|
| 観測と分類 | event-id, visible, timestamp, sensor-type |
| GPS位置 | location-lat, location-long |
| 鳥・機器の対応 | tag-local-identifier, individual-local-identifier, individual-taxon-canonical-name, study-name |
| 移動 | ground-speed, heading, height-above-ellipsoid |
| 位置精度・衛星数 | gps:dop, gps:satellite-count, eobs:horizontal-accuracy-estimate, eobs:speed-accuracy-estimate |
| その他 | eobs:temperature, eobs:battery-voltage, eobs:type-of-fix |

完全な26列のリストと各群の確認結果は[実測スキーマ集計JSON](../data/payoff_b_stork_gps_csv_header_result_20261124.json)に保存した。これは**列名があるという結果**であって、各列に有効な値が何件あるか、どの日付に撮れたか、同じ鳥が何年分あるかを検証した結果ではない。

## 原資料アクセスの段階

1. [PR #418](https://github.com/zuizui0223/payoff/pull/418)で3群の公開CC0アーカイブDOI・原本バンドル・README・参照CSVまで照合。
2. [PR #419](https://github.com/zuizui0223/payoff/pull/419)で開始日212/212、終了日欠損128、未来2030年の終了日1、タグ機器再使用と研究別個体識別子の問題を明示。
3. その後、新たな[4KiB部分取得契約](../data/payoff_b_stork_gps_zip_range_contract_20261124.json)に沿い、3群の原本GPS ZIPがHTTP 206で部分取得可能なことを確認。
4. [central directory契約](../data/payoff_b_stork_gps_zip_directory_contract_20261124.json)に従い、各ZIPの末尾65,557バイト以内からメンバー数・形式を検査。[ディレクトリ集計](../data/payoff_b_stork_gps_zip_directory_result_20261124.json)を保存。
5. [ヘッダー取得契約](../data/payoff_b_stork_gps_csv_header_contract_20261124.json)を事前に固定し、追加の厳格なRange制限下で大きなCSVの**最初の1行のみ**を技術スキーマとして取り出した。

ヘッダー抽出で元ソースから送られた圧縮データは、対照4,732バイト、遅延4,680バイト、自然出発4,358バイトに留まった（メタデータ・ローカルヘッダーの取得量を含む）。大量のイベントデータを展開・格納する操作をしていない。**ZIP本体の完全なMD5チェックサムは検証していない**ため、現時点で「GPSデータ全体が再現性確認済み」と呼ばない。

## 情報機構について未実証の項目

この成功により、実際のGPSレコードの時刻・位置・個体・機器を読むための**スキーマと効率的なアクセス経路**は明確になった。しかし、以下はまだ調べていない。

- 同じ個体に対して2020年の決定時点にどれだけGPS位置が存在し、移動していたか。
- 他個体の同時刻・同所的なGPS記録が独立に存在し、焦点個体の情報機会として利用可能だったか。
- 同じタグ機器の別の装着期間を混同せず、元の動物・装着イベントIDと正しく結合できるか。
- 事前の局所情報が将来の環境を予測する性能 q と、決定後に残っている移動・滞在の修正余地 r が独立に推定できるか。
- これらの値が元研究で既報の生存や戦略変更を超えて新規の生物学的説明力を持つか。

特に、Brønnvik et al. (2024, Current Biology, DOI 10.1016/j.cub.2024.03.052) は、同種個体の多い経路への選好と経験による依存低下を既に報告した。社会的接触機会だけを検証しても新規の情報×行動可能性の効果にはならない。

## 実行・再現証拠

- 一次資料：対照 [10.5441/001/1.271](https://doi.org/10.5441/001/1.271)、遅延 [10.5441/001/1.276](https://doi.org/10.5441/001/1.276)、自然出発 [10.5441/001/1.277](https://doi.org/10.5441/001/1.277)。
- 原本先頭4KBのRange実行：[Actions 45366891597](https://github.com/zuizui0223/payoff/actions/runs/45366891597)。
- 元ZIP索引の検証：[Actions 45367468782](https://github.com/zuizui0223/payoff/actions/runs/45367468782)。
- 元CSV先頭ヘッダーの検証：[Actions 45368226795](https://github.com/zuizui0223/payoff/actions/runs/45368226795)。元索引とヘッダーの2つの専用ジョブがSUCCESS。
- 原本索引集計アーティファクトID 14908665385（ZIP SHA256 8fbbf9e0e6beb912ac415b07e9267886860763a19d7b4a739dea692aa649da58）、ヘッダー集計ID 14908700481（ZIP SHA256 f8b53e294061e9910ffdd221f18b8db1dafc34a27f0af15d0403c304131d42c6）。
- [技術的実行コード](../scripts/payoff_b_stork_gps_csv_header_gate_20261124.py)と[安全性テスト](../tests/test_payoff_b_stork_gps_csv_header_gate_20261124.py)。

元の位置座標、観測個別時刻、元タグ名、元CSVの観測行、ZIPファイル全体はGitHubにコミットしていない。eBird・TinyFish未使用、mainと凍結原稿は未変更。

**判定：ORIGINAL_GPS_SCHEMA_SOURCE_PASS、TEMPORAL_JOINT_OBSERVATION_AND_INFORMATION_Q_NOT_YET_ESTIMATED。**
