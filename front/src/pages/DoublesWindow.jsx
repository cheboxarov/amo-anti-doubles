import { fetchDoubles } from '../api/doublesApi';
import { useSignals } from "@preact/signals-react/runtime";
import DoublesContainer from '../components/DoublesContainer/DoublesContainer';
import styles from './DoublesWindow.module.css';
import Spinner from '../components/spinner/Spinner';
import Header from '../components/Header/Header';
import { loading, doubles } from '../signals/doublesSignals';


const DoublesWindows = () => {
    useSignals()

    return (
        <div className={styles.App}>
            <Header />
            {loading.value ? <Spinner /> : Object.keys(doubles.value).length > 0 ? <DoublesContainer /> : null}
        </div>
    );
};

export default DoublesWindows;
